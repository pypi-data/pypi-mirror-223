from enum import Enum


class FlowModuleValue2Type0Language(str, Enum):
    DENO = "deno"
    PYTHON3 = "python3"
    GO = "go"
    BASH = "bash"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    GRAPHQL = "graphql"
    NATIVETS = "nativets"

    def __str__(self) -> str:
        return str(self.value)
