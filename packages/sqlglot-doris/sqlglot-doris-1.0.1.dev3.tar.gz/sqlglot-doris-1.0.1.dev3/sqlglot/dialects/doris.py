from __future__ import annotations

from sqlglot import exp
from sqlglot.dialects.dialect import (
    approx_count_distinct_sql,
    arrow_json_extract_sql,
    rename_func,
)
from sqlglot.dialects.mysql import MySQL
from sqlglot.helper import seq_get
from sqlglot.tokens import TokenType

class Doris(MySQL):
    class Parser(MySQL.Parser):
        FUNCTIONS = {
            **MySQL.Parser.FUNCTIONS,
            "DATE_TRUNC": lambda args: exp.TimestampTrunc(
                this=seq_get(args, 1), unit=seq_get(args, 0)
            ),
            "SYSDATE": TokenType.CURRENT_TIMESTAMP,
        }

    class Generator(MySQL.Generator):
        CAST_MAPPING = {
            exp.DataType.Type.BIGINT: "BIGINT",
            exp.DataType.Type.BOOLEAN: "BOOLEAN",
            exp.DataType.Type.INT: "INT",
            exp.DataType.Type.TEXT: "STRING",
            exp.DataType.Type.UBIGINT: "UNSIGNED",
            exp.DataType.Type.VARCHAR: "VARCHAR",
            exp.DataType.Type.BINARY: "STRING",
            exp.DataType.Type.BIT: "BOOLEAN",
            exp.DataType.Type.DATETIME64: "DATETIME",
            exp.DataType.Type.ENUM: "STRING",
            exp.DataType.Type.IMAGE: "UNSUPPORTED",
            exp.DataType.Type.INT128: "LARGEINT",
            exp.DataType.Type.INT256: "STRING",
            exp.DataType.Type.UINT128: "STRING",
            exp.DataType.Type.JSONB: "JSON",
            exp.DataType.Type.LONGTEXT: "STRING",
            exp.DataType.Type.MONEY: "DECIMAL",
        }

        TYPE_MAPPING = {
            **MySQL.Generator.TYPE_MAPPING,
            exp.DataType.Type.TEXT: "STRING",
            exp.DataType.Type.TIMESTAMP: "DATETIME",
            exp.DataType.Type.TIMESTAMPTZ: "DATETIME",
        }

        TRANSFORMS = {
            **MySQL.Generator.TRANSFORMS,
            exp.ApproxDistinct: approx_count_distinct_sql,
            exp.JSONExtractScalar: arrow_json_extract_sql,
            exp.JSONExtract: arrow_json_extract_sql,
            exp.DateDiff: rename_func("DATEDIFF"),
            exp.RegexpLike: rename_func("REGEXP"),
            exp.Coalesce: rename_func("NVL"),
            exp.CurrentTimestamp: lambda self, e: "NOW()",
            exp.TimeToStr: lambda self, e: f"DATE_FORMAT({self.sql(e, 'this')}, {self.format_time(e)})",
            # exp.StrToUnix: rename_func("UNIX_TIMESTAMP"),
            exp.StrToUnix: lambda self, e: f"UNIX_TIMESTAMP({self.sql(e, 'this')}, {self.format_time(e)})",
            exp.TimestampTrunc: lambda self, e: self.func(
                "DATE_TRUNC", exp.Literal.string(e.text("unit")), e.this
            ),
            exp.TimeStrToDate: rename_func("TO_DATE"),
            exp.UnixToStr: lambda self, e: f"FROM_UNIXTIME({self.sql(e, 'this')}, {self.format_time(e)})",
            exp.UnixToTime: rename_func("FROM_UNIXTIME"),
        }

        # TRANSFORMS.pop(exp.DateTrunc)
