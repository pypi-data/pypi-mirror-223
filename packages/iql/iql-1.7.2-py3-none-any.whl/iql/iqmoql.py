# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import sqlparse
import importlib
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple, Callable
from pandas import DataFrame
import pandas as pd
from abc import abstractmethod
from iql.q_cache_base import QueryCacheBase
from iql import options_parser
from iql import threading_experimental as te
import json

# Cache Settings
# Use iqmoql.activate_cache() before first execute() to
# ensure settings propogate to individual extensions.
# Infinite in memory cache by default

DEFAULT_EXT_DIRECTORY = None

# DB_MODULE is loaded on first call to get_dbmodule()
# Replace this string with another connector prior to first use,
# or set _DBCONNECTOR to None after changing.
DB_MODULE: str = "iql.db_connectors.duckdb_connector"

_EXTENSIONS: Dict[Tuple[str, str], "IqlExtension"] = {}
_DBCONNECTOR: Optional["IqlDatabaseConnector"] = None

# Used internally to name the dataframes
_DFPREFIX: str = "iqldf"

CACHE = QueryCacheBase()

# Add extensions via register_extension()
# Extensions are loaded on first access, to avoid requiring
# unused dependencies
_KNOWN_EXTENSIONS: Dict[str, str] = {
    "bql": "iql.bbg_bql.bql_extension",
    "s3": "iql.extensions.aws_s3_extension",
    "fred": "iql.extensions.fred_extension",
    "kaggle": "iql.extensions.kaggle_extension",
    "edgar": "iql.extensions.edgar_extension",
    "pandas": "iql.extensions.pandas_extension",
    "cache": "iql.extensions.cache_extension",
}

_ALIASES: Dict[
    str, Callable[[], str]
] = {}  # Callable, so we can either use text or external files

logger = logging.getLogger(__name__)


default_cache_policy_toplevel = {
    "max_age": 3600,
    "s3": False,
    "fcache": False,
    "memory": False,
}

default_cache_policies_keywords = {
    "bql": {"max_age": 3600, "fcache": True, "memory": True}
}


def get_policy_from_query(string: str) -> Optional[Dict[str, object]]:
    matches = re.search(r"cache\{(.+?)\}\s*\n", string)

    if matches:
        extracted_value = matches.group(1)
        logger.info(f"Query has policy: {extracted_value}")

        return dict(json.loads(f"{{{extracted_value}}}"))

    return {}


def _find_closing_paren(text: str, start: int) -> int:
    # TODO: Handle escaping
    paren_depth = 1
    quote_stack = []
    for i in range(start, len(text)):
        c = text[i]
        if c == "(" and len(quote_stack) == 0:
            paren_depth += 1
        elif c == "'" or c == '"':
            if len(quote_stack) == 0:
                quote_stack.append(c)
            elif quote_stack[len(quote_stack) - 1] == c:
                quote_stack.remove(c)
        elif c == ")" and len(quote_stack) == 0:
            paren_depth -= 1

        if paren_depth == 0:
            end = i
            return end
    raise ValueError("Never found closing parenthesis, probably unbalanced query")


def get_keyword_list(keywords: Optional[List[str]] = None) -> str:
    if keywords is None:
        keywords = list(_KNOWN_EXTENSIONS.keys())
    _keyword_list = "|".join((k if isinstance(k, str) else k[0] for k in keywords))
    return _keyword_list


def _extract_subquery_strings(
    query, keywords: Optional[List[str]] = None
) -> List[Tuple[str, str, str, str]]:
    global _cached_pats
    """Finds the subqueries start with keyword, along with matching end paren
    keyword(....)
    keyword.subword(....)
    """
    _keyword_list = get_keyword_list(keywords)

    _kpat = re.compile(rf"(?s)({_keyword_list})(\.(\w+))?\s*\(")

    results = []
    for m in re.finditer(_kpat, query):
        keyword = m.group(1)
        subword = m.group(3)
        paren_start = m.end()  # just after the last paren

        paren_end = _find_closing_paren(query, paren_start)

        outer = query[m.start() : paren_end + 1]
        inner = query[paren_start : paren_end + 1]
        logger.debug(
            f"Extracted subquery: {keyword}.{subword} at {paren_start}:{paren_end}"
        )

        results.append((keyword, subword, outer, inner))

    return results


@dataclass
class IqlResult:
    name: str
    query: str

    def arrow(self):
        pass

    def df_numpy(self):
        pass

    def df_arrow(self):
        pass

    def native(self):
        """Returns whatever the internal representation"""
        pass


@dataclass
class IqlResultData(IqlResult):
    name: str
    query: str
    _data: object

    def native(self):
        """Returns whatever the internal representation"""
        return self._data

    def arrow(self):
        raise ValueError("Not Implemented")

    def df_numpy(self):
        raise ValueError("Not Implemented")

    def df_arrow(self):
        raise ValueError("Not Implemented")


class IqlDatabase:
    @abstractmethod
    def execute_query(
        self, query: str, completed_results: List[IqlResult]
    ) -> Optional[IqlResult]:
        raise ValueError("Implement Me")

    @abstractmethod
    def get_connection(self) -> object:
        raise ValueError("Implement Me")

    @abstractmethod
    def close_db(self):
        raise ValueError("Implement Me")


class IqlDatabaseConnector:
    @abstractmethod
    def create_database(self) -> IqlDatabase:
        raise ValueError("Implement Me")

    @abstractmethod
    def create_database_from_con(self, con: object) -> IqlDatabase:
        raise ValueError("Implement Me")


_lasttoken = None


def get_subqueries_flat(queries: List["SubQuery"]) -> List["SubQuery"]:
    subqueries_flat = [
        q_inner for q_outer in queries for q_inner in q_outer.get_subqueries_flat()
    ]
    return subqueries_flat


@dataclass
class IqlExtension:
    keyword: str
    subword: str = field(default=None, init=True)  # type: ignore

    # Extensions must be parallelizable, or must
    # implement their own execute_batch.
    # Can only contain pickleable elements
    # etc

    # Determines whether the local cache settings should be used
    # vs  CACHE_PERIOD and
    # USE_FILE_CACHE
    temp_file_directory: Optional[str] = field(default=None, init=False)

    def get_output_dir(self) -> str:
        tempdir = (
            self.temp_file_directory if self.temp_file_directory is not None else "./"
        )
        return tempdir

    def allow_cache_read(self, sq: "SubQuery") -> bool:
        """Dont use cached values"""
        if sq.options.get("nocache") is True:
            return False
        elif sq.options.get("cache") is not None:
            return True
        else:
            return True

    def allow_cache_save(self, sq: "SubQuery") -> bool:
        return self.allow_cache_read(sq)

    def use_path_replacement(self) -> bool:
        """Some extensions just return a filestring to use instead of the SubQuery, such as the
        S3 Extension. If execute() returns None, then use_path_replacement must be used.
        """
        return False

    def get_path_replacement(
        self, subquery: "SubQuery", quote: bool = True
    ) -> Optional[str]:
        """Quoting is done here, with the expectation that some path replacements might actually be function calls."""
        tempdir = self.get_output_dir()
        filepath = f"{tempdir}/{subquery.name}.parquet"

        if quote:
            outpath = f"'{filepath}'"
        else:
            outpath = filepath

        logger.info(f"Converted {subquery} to {outpath}")
        return outpath

        """Used for extensions which use a native duckdb extension to access the underlying data"""
        return None

    @abstractmethod
    def executeimpl(self, sq: "SubQuery") -> Optional[DataFrame]:
        raise ValueError("Implement Me")

    def execute(self, sq: "SubQuery") -> Optional[DataFrame]:
        # usage: select * from (verityapi(functionname, targetname)) as verityquery
        # An empty response means no response was needed
        # Internal failure must raise an exception
        if sq.populate_from_cache() and sq.dataframe is not None:
            return sq.dataframe

        logger.debug(f"Executing query {sq.subquery}")

        df = self.executeimpl(sq)

        if df is None and not self.use_path_replacement():
            raise ValueError("Empty DF, should never reach here")
        else:
            if df is not None:
                pivot_options = sq.options.get("pivot")
                melt_options = sq.options.get("melt")

                df = self.apply_pandas_operations_prepivot(df, sq.options)

                if pivot_options is not None:
                    df = self.pivot(df, pivot_options)  # type: ignore
                if melt_options is not None:
                    df = df.melt(melt_options)

                df = self.apply_pandas_operations_postpivot(df, sq.options)

                sq.dataframe = df

                sq.save_to_cache()

                return df

    def execute_batch(
        self,
        queries: List["SubQuery"],
        cache_policy: Optional[Dict[str, object]] = None,
    ) -> List[IqlResult]:
        """Default implementation runs individually, override for functions that can be batched, such as
        BQL's _many functions.
        Executes all subqueries first, then merges as required.
        SubQueries are executed in a threadpool, which has minimal benefit."""

        completed_results = []
        # context = get_context('spawn')

        subqueries_flat = get_subqueries_flat(queries)
        # Get all the queries (and any queries inside SubQueryGroups)

        # Executes the ungrouped queries

        if te.ENABLED and te.MAX_PROCESSES > 1 and len(queries) > 1:
            te.execute_batch(subqueries_flat, self.execute, cache_policy)
        else:
            for query in subqueries_flat:
                try:
                    self.execute(query)  # type: ignore
                except Exception as e:
                    raise ValueError(f"Error from {query}") from e

        # Merge the results
        for query in queries:
            # For single subqueries, this is a noop
            # For subquery groups, this merges the results of the children
            query.merge()

            df = query.dataframe
            if df is None and not self.use_path_replacement():
                q = "Unknown"
                try:
                    q = query.get_query()
                except Exception:
                    pass
                raise ValueError(f"Empty DF, {q} failed")

            elif df is None:
                logger.debug("Using path replacement, no DF")
            else:
                query.dataframe = df  # type: ignore

                ir = IqlResultData(name=query.name, query=query.subquery, _data=df)
                completed_results.append(ir)

        return completed_results

    def create_subquery(
        self, subquery: str, name: str, iqc: "IqlQueryContainer"
    ) -> "SubQuery":
        logger.debug("Creating subquery")
        sq = SubQuery(extension=self, subquery=subquery, name=name, iqc=iqc)
        return sq

    def create_subqueries(
        self,
        query: str,
        name: str,
        iqc: "IqlQueryContainer",
        create_function: Optional[Callable] = None,
    ) -> List["SubQuery"]:
        """Converted to always return a single item, but left logic in place to support multiple"""
        logger.debug(f"Creating a subquery {name[:50]} for {query[:50]}")

        if create_function is None:
            create_function = self.create_subquery

        sq = create_function(subquery=query, name=name, iqc=iqc)

        # If a paramlist is passed, create one subquery for each value

        if "paramquery" in sq.options:
            paramquery: Tuple[str, str] = sq.options.get("paramquery")  # type: ignore

            if (
                len(paramquery) == 2
                and isinstance(paramquery[0], str)
                and isinstance(paramquery[1], str)
            ):
                parameter_name = paramquery[0]
                param_query = paramquery[1]
                result = iqc.db.execute_query(param_query, completed_results=[])  # type: ignore

                df = result.df_numpy()
                parameter_values = df[df.columns[0]].values
                logger.debug(f"Values {parameter_values}")
            else:
                raise ValueError(f"Invalid options passed to paramquery: {paramquery}")

        elif "paramlist" in sq.options:
            paramlist: Tuple[str, List[str]] = sq.options.get("paramlist")  # type: ignore

            if not isinstance(paramlist, list) and len(paramlist) != 2:
                raise ValueError("paramlist must be a Tuple of (param, [values])")

            parameter_name = paramlist[0]
            parameter_values: List[str] = paramlist[1]
            logger.debug(f"Found paramlist: {parameter_name} => {parameter_values}")

            if parameter_values is None or len(parameter_values) == 0:
                raise ValueError("Empty values passed to paramlist passed")

            if isinstance(parameter_values, str):
                parameter_values = [parameter_values]
        else:
            parameter_name = None
            parameter_values = None  # type: ignore

        if parameter_name is not None:
            if parameter_values is None or len(parameter_values) == 0:
                parameter_values = {None}  # type: ignore
                # raise ValueError(f"{parameter_name}: No parameter values passed for query: {query}")

            sqs: List["SubQuery"] = []
            count = 1

            if not parameter_name.startswith("$"):
                logger.debug("Parameter name doesn't start with $, inserting one")
                # This is helpful to avoid replacing the paramquery when substituting
                parameter_name = f"${parameter_name}"

            for v in parameter_values:
                v_query = query.replace(parameter_name, str(v))

                sq = create_function(  # type: ignore
                    subquery=v_query, name=f"{name}_{count}", iqc=iqc
                )

                sqs.append(sq)
                count += 1

            sq_group = SubQueryGroup(
                subqueries=sqs,
                extension=self,
                subquery=name,  # subqueries are ignored for subquerygroups
                name=f"{name}_group",
                iqc=iqc,
            )

            return [sq_group]
        else:
            return [sq]

    def fix_col_ref(self, opt: str, columns: List[str]):
        if opt in columns:
            return opt
        opt_l = opt.lower().strip()
        opt_ci = next((c for c in columns if c.lower() == opt_l), None)

        if opt_ci is None:
            raise ValueError(f"{opt} not in columns: {columns}")

        return opt_ci

    def apply_pandas_operations_postpivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:
        fillna_opt: str = options.get("fillna")  # type: ignore
        if fillna_opt is not None:
            working_df = working_df.fillna(fillna_opt)

        dropna_opt = options.get("dropna")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def apply_pandas_operations_prepivot(
        self, working_df, options: Dict[str, object]
    ) -> DataFrame:
        # only drops from the "value" column
        fillna_opt: str = options.get("fillna_pre")  # type: ignore
        if fillna_opt is not None:
            logger.debug(f"Filling NaNs with in value column with {fillna_opt}")
            working_df["value"] = working_df["value"].fillna(fillna_opt)

        dropna_opt = options.get("dropna_pre")
        logger.debug(f"Dropping NA from column {dropna_opt}")
        if isinstance(dropna_opt, bool) and dropna_opt is True:
            working_df = working_df.dropna()
        elif isinstance(dropna_opt, str):
            working_df = working_df.dropna(subset=[dropna_opt])
        elif isinstance(dropna_opt, list):
            working_df = working_df.dropna(subset=dropna_opt)

        return working_df

    def pivot(self, working_df: DataFrame, pivot_option: Union[str, List]) -> DataFrame:
        if pivot_option is None:
            return working_df

        # isauto = False
        logger.debug(f"Pivoting by {pivot_option}")
        if isinstance(pivot_option, str):
            if pivot_option.lower() == "none":
                # Pivot disabled / noop
                return working_df
            elif pivot_option.lower() == "auto":
                # isauto = True
                index = []
                column = "name"
                value = "value"

                if column not in working_df.columns or value not in working_df.columns:
                    raise ValueError(
                        f"{column} or {value} not found in dataframe columns. Auto should only be used with BQL results."
                    )

                fieldsToCheck = [
                    "id",
                    "orig_ids",
                    "orig_ids:0",
                    "period",
                    "as_of_date",
                    "date",
                ]
                lower_cols = [col.lower() for col in working_df.columns]
                allcols = list(working_df.columns)

                # Case insensitive lookup, but then create an index from the case sensitive names
                for f in fieldsToCheck:
                    if f in lower_cols:
                        index.append(allcols[lower_cols.index(f)])

                if len(index) == 0:
                    index = index[0]
            else:
                raise ValueError("Unexpected pivot setting {pivot_option}")
        elif len(pivot_option) != 2 and len(pivot_option) != 3:
            raise ValueError(f"Unexpected size for pivot options {pivot_option}")
        else:
            index = pivot_option[0]
            column = pivot_option[1]
            value = pivot_option[2] if len(pivot_option) == 3 else "value"

            if index == "auto":
                used_cols = [column.lower(), value.lower()]
                # Use all columns except column and value
                index = [
                    col for col in working_df.columns if col.lower() not in used_cols
                ]
        cols: List[str] = list(working_df.columns)  # type: ignore

        if isinstance(index, list):
            index = [self.fix_col_ref(i, cols) for i in index]
            if len(index) == 1:
                index = index[0]
        else:
            index = self.fix_col_ref(index, cols)

        if isinstance(column, list):
            column = [self.fix_col_ref(i, cols) for i in column]
            if len(column) == 1:
                column = column[0]
        else:
            column = self.fix_col_ref(column, cols)

        if isinstance(value, list):
            value = [self.fix_col_ref(i, cols) for i in value]
            if len(value) == 1:
                value = value[0]
        else:
            value = self.fix_col_ref(value, cols)

        if isinstance(column, list):
            # Needed to allow pivoting by datetime columns
            for col in column:
                if pd.api.types.is_datetime64_any_dtype(working_df[col]):
                    working_df[col] = working_df[col].dt.strftime("%Y-%m-%d")

        logger.debug(f"Pivot index {index} columns {column} values {value}")

        working_df = working_df.pivot_table(
            index=index, columns=column, values=value, aggfunc="last", dropna=False
        )

        working_df = working_df.reset_index()

        if isinstance(value, list) and len(value) > 1:
            working_df.columns = [
                "_".join(reversed(str(col) if type(col) == int else col))
                for col in working_df.columns.values
            ]
        elif isinstance(column, list) and len(column) > 1:
            # Flatten multicolumn indices
            working_df.columns = [
                "_".join(str(col) if type(col) == int else col)
                for col in working_df.columns.values
            ]

        # Clean columns
        renames = {}
        for col in working_df.columns:
            # assert isinstance(col, str)
            colname = col
            newcol = (
                str(colname)
                .replace("#", "")
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "_")
            )
            newcol = newcol.strip("_")
            if col != newcol:
                # columns can't have #, ( or ) symbols
                # logger.debug(f"Replacing {col} with {newcol}")
                renames[col] = newcol

        if len(renames) > 0:
            working_df = working_df.rename(columns=renames)

        return working_df


@dataclass
class SubQuery:
    extension: IqlExtension
    subquery: str
    name: str
    iqc: "IqlQueryContainer"
    dataframe: Optional[DataFrame] = field(default=None, init=False)
    cache_policy: Optional[Dict[str, object]] = field(default=None, init=False)
    options: Dict[str, object] = field(default_factory=dict, init=False)
    input_data: object = field(default=None, init=False)

    local_dfs: Dict[str, object] = field(default_factory=dict, init=False)

    def get_subqueries_flat(self) -> List["SubQuery"]:
        return [self]

    def merge(self):
        # Nothing to do for a single subquery
        pass

    def get_query(self) -> str:
        """Returns the first parameter to:
        keyword(query, *params)"""
        if len(self.options) == 0:
            raise ValueError(f"Options not properly passed or parsed ({self.subquery})")

        query = next(iter(self.options.keys()))
        return query

    def __post_init__(self):
        try:
            if self.subquery is not None:
                self.options: Dict[str, object] = options_parser.options_to_list(
                    self.subquery
                )
                # logger.debug(f"Options: {str(self.options)[:50]}")
        except Exception:
            logger.exception(f"Exception in {str(self.subquery)[:50]}")
            raise ValueError(f"Parse Exception of {str(self.subquery)[:50]}")

    def populate_from_cache(self) -> bool:
        """Returns cached value if it's available"""
        cache_val = self.subquery

        logger.debug(f"Checking cache for {str(cache_val)[:50]}, {type(self)}")
        if not self.extension.allow_cache_read(self):
            return False

        df = CACHE.get(key=cache_val, policy=self.cache_policy)
        if df is not None:
            logger.debug("Using cached SubQuery")
            self.dataframe = df  # type: ignore
            return True
        else:
            logger.debug("Not found in cache")
            return False

    def save_to_cache(self):
        if not self.extension.allow_cache_save(self):
            return

        cache_val = self.subquery

        if self.dataframe is not None:
            CACHE.save(key=cache_val, data=self.dataframe, policy=self.cache_policy)


@dataclass
class SubQueryGroup(SubQuery):
    """SubQueryGroups represent a set of queries whose outputs will be combined.
    SubQueries are executed in parallel (via get_subqueries_flat),
    so this step is needed to gather the results.

    Our first implementation was to rely on database Unions, but performance wasn't
    great.

    Future: SubQueryGroups could support nesting, only one level supported now."""

    subqueries: List[SubQuery]

    def __post_init__(self):
        self.subquery = None  # type: ignore
        self.options = None  # type: ignore

    def get_subqueries_flat(self) -> List[SubQuery]:
        return self.subqueries

    def get_query(self) -> str:
        raise ValueError("SubQueryGroups do not have a query")

    def merge(self):
        """Since each file may have a different schema, we'll read them all and let's Pandas concat
        sort it out. Using DuckDb "union by name" ran into an error (hash table memory)
        """

        if self.extension.use_path_replacement():
            files = [
                self.extension.get_path_replacement(sq, quote=False)
                for sq in self.subqueries
            ]

            logger.info(f"Read {len(files)} parquet files")

            dfs = [pd.read_parquet(f) for f in files]
            logger.info("Done reading, concatting")

            df = pd.concat(dfs)

            outfile = self.extension.get_path_replacement(self, quote=False)
            logger.info(f"Writing to final parquet file {outfile}")

            df.to_parquet(outfile)

        else:
            dfs: List[DataFrame] = [sq.dataframe for sq in self.subqueries]  # type: ignore
            logger.debug(f"Concatting {len(dfs)}")
            if len(dfs) == 1:
                self.dataframe = dfs[0]
            else:
                self.dataframe = pd.concat(dfs)

        logger.info(f"Done merging {len(self.subqueries)} subqueries")


class IqlQueryContainer:
    # This is used so we can run the bql_queries as an async batch, separate from processing the results.
    orig_query: str
    query: str
    subqueries: List[SubQuery]
    db: Optional[object]
    cache_policy: Optional[Dict[str, object]] = None

    def extract_subqueries(self):
        subqueries: List[SubQuery] = []

        i = 0

        replacements: Dict[str, Optional[str]] = {}

        if "--" in self.orig_query:
            query = sqlparse.format(self.orig_query, strip_comments=True).strip()
        else:
            query = self.orig_query

        for keyword, subword, outer, inner in _extract_subquery_strings(query):
            i += 1
            name = f"{_DFPREFIX}_{i}"

            extension = get_extension(keyword, subword)
            sqs: List[SubQuery] = extension.create_subqueries(
                query=outer, name=name, iqc=self
            )
            subqueries.extend(sqs)

            if extension.use_path_replacement():
                names = [sq.extension.get_path_replacement(sq) for sq in sqs]
            else:
                names = [sq.name for sq in sqs]

            if len(names) == 1:
                result = names[0]
            else:
                querystrings = [f"(select * from {i})" for i in names]

                result = " UNION ".join(querystrings)
                result = f"({result})"

            replacements[outer] = result

        for old, new in replacements.items():
            logger.debug(f"Replacing {str(old)[:50]} with {str(new)[:50]}")
            query = query.replace(old, new)  # type: ignore

        # if only one function without a beginning subquery
        if len(replacements) > 0:
            values = [value for value in replacements.values() if value is not None]
            if re.match(rf"(?s)\s*({'|'.join(values)}).*", query) is not None:
                logger.info(f"Starts with replacement {values}")
                query = f"select * from {query}"

        self.query = query

        return subqueries

    def __init__(self, query: str, db: IqlDatabase):
        self.orig_query = query
        self.query = query
        self.db = db

        self.cache_policy = get_policy_from_query(query)
        if self.cache_policy is None:
            self.cache_policy = default_cache_policy_toplevel

        self.subqueries = self.extract_subqueries()
        # self.subqueries = self._extract_replacements()
        # Sanity checks. These don't take into account escaping or quoting, so they're just warnings.
        if query.count("(") != query.count(")"):
            logger.warning("Left and Right Paren counts aren't equal")

        if query.count("'") % 2 != 0:
            logger.warning("Uneven number of single quotes")

        if query.count('"') % 2 != 0:
            logger.warning("Uneven number of double quotes")

    def get_subqueries_by_extension(self, keyword: str, subword: str) -> List[SubQuery]:
        results: List[SubQuery] = []
        results = [
            s
            for s in self.subqueries
            if s.extension.keyword == keyword and s.extension.subword == subword
        ]

        return results

    def execute(self) -> Tuple[Optional[DataFrame], List[IqlResult]]:
        """Returns the final df, plus the intermediate subquery dataframes.
        If the query is not a Select, returns a None"""
        # Execute the subqueries

        completed_results: List[IqlResult] = []

        logger.debug(f"checking cache {self.orig_query}, {self.cache_policy}")
        df = CACHE.get(key=self.orig_query, policy=self.cache_policy)
        if df is not None:
            logger.debug("Query found fully in cache, using.")
            return (df, [])

        for (keyword, subword), e in _EXTENSIONS.items():
            sqs: List[SubQuery] = self.get_subqueries_by_extension(keyword, subword)  # type: ignore

            # If the cache policy has a policy for the subtype, use that, otherwise use defaults
            # Don't use the top level cache policy
            sub_policy: Optional[Dict[str, object]] = (  # type: ignore
                self.cache_policy.get(keyword, None)
                if self.cache_policy is not None
                else None
            )
            if sub_policy is None:
                sub_policy = default_cache_policies_keywords.get(keyword, None)  # type: ignore

            if sub_policy is not None:
                for q in sqs:
                    q.cache_policy = sub_policy  # type: ignore

                    if hasattr(q, "subqueries"):
                        for sqq in q.subqueries:  # type: ignore
                            sqq.cache_policy = sub_policy  # type: ignore

            try:
                e_results = e.execute_batch(sqs, sub_policy)  # type: ignore
            except Exception as e:
                raise ValueError(
                    f"Failed to execute batch {keyword} {subword}: {self.query} {sqs}"
                ) from e
            completed_results += e_results

        result = self.db.execute_query(query=self.query, completed_results=completed_results)  # type: ignore

        if result is None:
            df = None
        else:
            df = result.df_numpy()

        # add the final result to the completions
        final_result = IqlResultData(name="final", query=self.query, _data=df)  # type: ignore

        completed_results.append(final_result)

        CACHE.save(key=self.orig_query, data=df, policy=self.cache_policy)

        return (df, completed_results)  # type: ignore


class IqlPlan:
    pass


def _parameterize_sql_alias(subword, query) -> str:
    if subword not in _ALIASES.keys():
        raise ValueError(f"Unknown alias {subword}")

    base_query_gen = _ALIASES[subword]
    base_query = base_query_gen()

    for k, v in options_parser.options_to_list(query).items():
        # convert the parameter to $uppercase, so security => $SECURITY
        newk = f"${k.upper()}"
        base_query = base_query.replace(newk, str(v))

    return base_query


def replace_sql_aliases(query) -> str:
    newquery = query
    for keyword, subword, outer, inner in _extract_subquery_strings(query, ["alias"]):
        sql = _parameterize_sql_alias(subword, outer)

        # aliases might recurse
        sql = replace_sql_aliases(sql)
        logger.debug(f"Found SQL alias, replacing and parameterizing: {outer}")

        newquery = newquery.replace(outer, sql)
        # logger.info(f"After alias replacement {query}")

    return newquery


def execute_debug(
    query: str, con: Optional[object] = None, params: Optional[Dict[str, object]] = None
) -> Tuple[bool, Optional[DataFrame], Optional[Dict[str, List[IqlResult]]]]:
    """Returns the success (True or False), final query result, and the debug results: all the intermediate queries and subqueries."""
    # Connection to database

    # TODO: Get rid of this special case for BQL only.
    if query.strip().startswith("get") or query.strip().startswith("let"):
        query = query.replace('"', '"')
        query = f"""select * from bql("{query}")"""

    # Initialize or Reuse DB Connector
    get_dbconnector()
    if _DBCONNECTOR is None:
        raise ValueError("DBConnector Not Set")
    if con is None:
        db = _DBCONNECTOR.create_database()
    else:
        db = _DBCONNECTOR.create_database_from_con(con=con)

    if params is not None:
        logger.info(f"Parameterizing with {params}")
        for k, v in params.items():
            query = query.replace(f"${k.upper()}", str(v))

    # Aliases
    query = replace_sql_aliases(query)

    try:
        # A single query might contain multiple SQL statements. Parse them out and iterate:
        df = None
        completed_result_map = {}
        if ";" not in query:
            # Performance optimization for simple queries
            iqc = IqlQueryContainer(query=query, db=db)

            df, completed_results = iqc.execute()
            return (True, df, {query: completed_results})
        else:
            for statement in sqlparse.parse(query):
                singlequery = statement.value.strip(";")
                iqc = IqlQueryContainer(query=singlequery, db=db)

                # Run each statement, but only keep the results from the last one
                df, completed_results = iqc.execute()

                completed_result_map[statement] = completed_results

        return (True, df, completed_result_map)

    finally:
        if con is None:  # DB was created here, so close it
            db.close_db()


def execute(
    query: str, con: Optional[object] = None, params: Optional[Dict[str, object]] = None
) -> Optional[DataFrame]:
    """Executes the given SQL query. Keyword is only used to run a single subquery without SQL."""

    success, df, completed_results = execute_debug(query, con, params=params)

    return df


def get_dbconnector() -> IqlDatabaseConnector:
    global _DBCONNECTOR
    if _DBCONNECTOR is None:
        # Initializes only on first reference
        module = importlib.import_module(DB_MODULE)
        _DBCONNECTOR = module.getConnector()

    if _DBCONNECTOR is None:
        raise ValueError("Failure initializing _DBCONNECTOR")
    return _DBCONNECTOR


def register_extension(e: IqlExtension):
    _EXTENSIONS[(e.keyword, e.subword)] = e  # type: ignore
    if e.keyword not in _KNOWN_EXTENSIONS.keys():
        _KNOWN_EXTENSIONS[e.keyword] = e.keyword

    if e.temp_file_directory is None:
        e.temp_file_directory = DEFAULT_EXT_DIRECTORY


def register_alias(subword: str, sql: str, file: str):
    """
    Aliases are called via
    alias.aliasname(param1=abc, param2.abc)
    When run, the alias will be replaced, and "$PARAM1" will be replaced with abc.
    You can either register the entire SQL or a path to a file containing the SQL.
    If both are passed, the SQL is used/cached
    """

    logger.debug(f"Registering alias: {subword}")

    if sql is not None:
        _ALIASES[subword] = lambda: sql
    elif file is not None:
        _ALIASES[subword] = lambda: open(file).read()
    else:
        raise ValueError("register_alias: sql or file is None. One must be passed")


def list_extensions() -> List[str]:
    return list(_KNOWN_EXTENSIONS.keys())


def get_extension(keyword: str, subword: str) -> "IqlExtension":
    """Loads extension on first use"""

    words = (keyword, subword)
    if words in _EXTENSIONS:
        return _EXTENSIONS[words]
    elif keyword not in _KNOWN_EXTENSIONS.keys():
        raise ValueError(f"Unknown Extension {keyword}")
    else:
        # Dynamically load extensions on first use
        # This avoids requiring installation of packages that
        # aren't needed
        classname = _KNOWN_EXTENSIONS[keyword]
        module = importlib.import_module(classname)
        module.register(keyword)

        if words not in _EXTENSIONS:
            raise ValueError(f"{keyword}.{subword} is not registered")
        return _EXTENSIONS[words]


def get_cache():
    return CACHE


def set_cache(cache: QueryCacheBase):
    global CACHE
    CACHE = cache


def configure(
    temp_dir: Optional[str] = None,
    max_processes: Optional[int] = None,
):
    """
    Must be called before extensions are initialized (on first use)
    duration_seconds: None (Disabled), -1 (Infinite), int (Seconds)
    file_directory: None (no file cache), string (output directory)
    """
    global DEFAULT_EXT_DIRECTORY
    DEFAULT_EXT_DIRECTORY = temp_dir

    if max_processes is not None:
        te.MAX_PROCESSES = max_processes


def get_bql_default_policy():
    return default_cache_policies_keywords.get("bql", None)
