from typing import Any, Dict
import os 
import logging
from datetime import datetime
import json
import MySQLdb  
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()  
LOG_FILE = "logs.json"

mcp = FastMCP("mysql-server",log_level='ERROR')


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "test"),
    "passwd": os.getenv("DB_PASSWORD", "test"), 
    "db": os.getenv("DB_NAME", "test_db"),  
    "port": int(os.getenv("DB_PORT", 3306))
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mysql-mcp-server")
logging.basicConfig(level=logging.DEBUG)
query_logs = []  
FORBIDDEN_FIELDS = ["password", "salary"]

def has_forbidden_fields(sql: str) -> bool:
    sql_lower = sql.lower()
    for field in FORBIDDEN_FIELDS:
        if field in sql_lower:
            return True
    return False
INJECTION_PATTERNS = [
    "--",       # SQL注释
    "union ",   # 联合查询注入
    " or ",    # 常见条件绕过
    "' or '1'='1",  # 经典注入语句
    "sleep(",  # 时间盲注
    "benchmark(",
    "drop ",
    "insert ",
    "update ",
    "delete ",
    "exec ",
    "execute "
]

def contains_sql_injection(sql: str) -> bool:
    sql_lower = sql.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in sql_lower:
            return True
    return False

def get_connection():
    try:
        return MySQLdb.connect(**DB_CONFIG)
    except MySQLdb.Error as e:
        print(f"Database connection error: {e}")
        raise

def save_log(entry):
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save log: {e}")


@mcp.resource("mysql://schema")
def get_schema() -> Dict[str, Any]:
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [list(table.values())[0] for table in tables]

        schema = {}
        for table_name in table_names:
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = cursor.fetchall()
            table_schema = []

            for column in columns:
                table_schema.append({
                    "name": column["Field"],
                    "type": column["Type"],
                    "null": column["Null"],
                    "key": column["Key"],
                    "default": column["Default"],
                    "extra": column["Extra"]
                })

            schema[table_name] = table_schema

        return {
            "database": DB_CONFIG["db"],
            "tables": schema
        }
    finally:
        if cursor:
            cursor.close()
        conn.close()

def is_safe_query(sql: str) -> bool:
    sql_lower = sql.lower()
    unsafe_keywords = ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    return not any(keyword in sql_lower for keyword in unsafe_keywords)


@mcp.tool()
def query_data(sql: str) -> bool:
    sql_strip = sql.strip().lower()

    # 必须以 select 开头
    if not sql_strip.startswith("select"):
        return False

    # 不允许多条语句（这里简单判断是否有分号且非末尾）
    if ';' in sql_strip[:-1]:
        return False

    if has_forbidden_fields(sql):
        return {
            "success": False,
            "error": "Query contains forbidden fields like password or salary."
        }
    
    if contains_sql_injection(sql):
        return {"success": False, "error": "Query contains possible SQL injection patterns."}
    # return True
    logger.info(f"Executing query: {sql}")
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)        
        cursor.execute("SET TRANSACTION READ ONLY")
        cursor.execute("START TRANSACTION")
        
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.commit()
            
            query_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sql": sql
            })
            save_log(query_logs[-1])
            
            return {
                "success": True,
                "results": results,
                "rowCount": len(results)
            }
        except Exception as e:
            conn.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    finally:
        if cursor:
            cursor.close()
        conn.close()


@mcp.resource("mysql://tables")
def get_tables() -> Dict[str, Any]:
    """Provide database table list"""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [list(table.values())[0] for table in tables]
        
        return {
            "database": DB_CONFIG["db"],
            "tables": table_names
        }
    finally:
        if cursor:
            cursor.close()
        conn.close()

@mcp.resource("mysql://logs")
def get_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
    except Exception as e:
        logger.error(f"Failed to read log file: {e}")
        logs = []
    
    return {
        "count": len(logs),
        "logs": logs[-100:]
    }


def validate_config():
    """Validate database configuration"""
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.warning(f"Missing environment variables: {', '.join(missing)}")
        logger.warning("Using default values, which may not work in production.")


def main():
    validate_config()
    print(f"MySQL MCP server started, connected to {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}")


if __name__ == "__main__":
    main()
    mcp.run()

