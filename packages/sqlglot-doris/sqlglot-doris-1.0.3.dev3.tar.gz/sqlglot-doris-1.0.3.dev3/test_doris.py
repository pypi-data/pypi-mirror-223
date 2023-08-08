import sqlglot
import sqlparse

# sql_file_path = "./test_oracle.sql"
# with open(sql_file_path,"r") as sql_file:
#     sql_statements = sql_file.read()
#
# result = sqlglot.transpile(sql_statements, read="hive", write="doris")[0]
#
# formatted_sql = sqlparse.format(result, reindent=True, indent_tabs=False)
# sql_file_path_result = "./test_oracle_result.sql"
# with open(sql_file_path_result,"w") as sql_file_result:
#     sql_file_result.write(formatted_sql)

sql = """select from_unixtime(1196440219, '%Y-%m-%d %H:%i:%s');"""
result1 = sqlglot.transpile(sql, read="hive", write="doris")[0]
formatted_sql1 = sqlparse.format(result1, reindent=True, indent_tabs=False)
print(formatted_sql1)


