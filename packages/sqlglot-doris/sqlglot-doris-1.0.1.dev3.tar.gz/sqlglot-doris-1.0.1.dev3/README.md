![SQLGlot logo](sqlglot.svg)

SQLGlot is a no-dependency SQL parser, transpiler, optimizer, and engine. It can be used to format SQL or translate between [19 different dialects](https://github.com/tobymao/sqlglot/blob/main/sqlglot/dialects/__init__.py) like [DuckDB](https://duckdb.org/), [Presto](https://prestodb.io/), [Spark](https://spark.apache.org/), [Snowflake](https://www.snowflake.com/en/), and [BigQuery](https://cloud.google.com/bigquery/). It aims to read a wide variety of SQL inputs and output syntactically and semantically correct SQL in the targeted dialects.

It is a very comprehensive generic SQL parser with a robust [test suite](https://github.com/tobymao/sqlglot/blob/main/tests/). It is also quite [performant](#benchmarks), while being written purely in Python.

You can easily [customize](#custom-dialects) the parser, [analyze](#metadata) queries, traverse expression trees, and programmatically [build](#build-and-modify-sql) SQL.

Syntax [errors](#parser-errors) are highlighted and dialect incompatibilities can warn or raise depending on configurations. However, it should be noted that SQL validation is not SQLGlot’s goal, so some syntax errors may go unnoticed.

Learn more about the SQLGlot API in the [documentation](https://sqlglot.com/).

Contributions are very welcome in SQLGlot; read the [contribution guide](https://github.com/tobymao/sqlglot/blob/main/CONTRIBUTING.md) to get started!

Since the community has not had time to merge, temporarily package doris to use.

## Install

From PyPI:

```
pip3 install sqlglot-doris
```

## Examples

### Formatting and Transpiling

Easily translate from one dialect to another. For example, date/time functions vary between dialects and can be hard to deal with:

```python
import sqlglot
sqlglot.transpile("SELECT TIME_TO_STR('2020-01-01', '%Y-%m-%d')", read="hive", write="doris")[0]
```

```sql
SELECT DATE_FORMAT('2020-01-01', '%Y-%m-%d')
```

SQLGlot can even translate custom time formats:

```python
import sqlglot
sqlglot.transpile("SELECT UNIX_TO_STR(x, y)", read="hive", write="doris")[0]
```

```sql
"SELECT FROM_UNIXTIME(x, y)"
```

As another example, let's suppose that we want to read in a SQL query that contains a CTE and a cast to `REAL`, and then transpile it to Spark, which uses backticks for identifiers and `FLOAT` instead of `REAL`:

```python
import sqlglot

sql = """WITH baz AS (SELECT a, c FROM foo WHERE a = 1) SELECT f.a, b.b, baz.c, CAST("b"."a" AS REAL) d FROM foo f JOIN bar b ON f.a = b.a LEFT JOIN baz ON f.a = baz.a"""
print(sqlglot.transpile(sql, write="spark", identify=True, pretty=True)[0])
```

```sql
WITH `baz` AS (
  SELECT
    `a`,
    `c`
  FROM `foo`
  WHERE
    `a` = 1
)
SELECT
  `f`.`a`,
  `b`.`b`,
  `baz`.`c`,
  CAST(`b`.`a` AS FLOAT) AS `d`
FROM `foo` AS `f`
JOIN `bar` AS `b`
  ON `f`.`a` = `b`.`a`
LEFT JOIN `baz`
  ON `f`.`a` = `baz`.`a`
```

Comments are also preserved on a best-effort basis when transpiling SQL code:

```python
sql = """
/* multi
   line
   comment
*/
SELECT
  tbl.cola /* comment 1 */ + tbl.colb /* comment 2 */,
  CAST(x AS INT), # comment 3
  y               -- comment 4
FROM
  bar /* comment 5 */,
  tbl #          comment 6
"""

print(sqlglot.transpile(sql, read='doris', pretty=True)[0])
```

```sql
/* multi
   line
   comment
*/
SELECT
  tbl.cola /* comment 1 */ + tbl.colb /* comment 2 */,
  CAST(x AS INT), /* comment 3 */
  y /* comment 4 */
FROM bar /* comment 5 */, tbl /*          comment 6 */
```