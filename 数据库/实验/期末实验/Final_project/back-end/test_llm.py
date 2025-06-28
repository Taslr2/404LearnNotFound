import asyncio
from llm_interface import nl_to_sql

async def main():
    schema = schema = """
    students(id INT, name VARCHAR(50), age INT)
    courses(id INT, title VARCHAR(100))
    """
    question = input("请输入问题：")
    sql = await nl_to_sql(question, schema)           
    print("生成的SQL：", sql)

if __name__ == "__main__":
    asyncio.run(main())
