import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# 通义千问的API Key
QWEN_API_KEY = os.getenv("QWEN_API_KEY")

QWEN_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# prompt 模板
PROMPT_TEMPLATE = """
你是一个经验丰富的SQL生成助手，擅长将自然语言转换为正确的MySQL查询语句。请根据下面的自然语言问题生成对应的MySQL查询语句，**只返回最终的 SQL 代码，不需要解释说明**。

你需要特别注意以下几点：
1. 支持使用 JOIN、GROUP BY、HAVING 等 SQL 高级语法。
2. 结合数据库结构，准确理解问题中的逻辑，例如“多个”“至少一个”“没有”等。
3. SQL中使用的表和字段必须来自以下数据库结构。
4. 返回的语句必须是标准 MySQL SELECT 语句，不包含 INSERT、UPDATE 等操作。
5. 请优化语句结构，尽量避免低效的嵌套子查询、冗余的 IN 子句，优先使用 JOIN 等高效方式提升查询性能。

以下是一些示例供你参考：

【示例1】
数据库结构：
student(s_ID, name)
advisor(s_ID, i_ID)

自然语言问题：
Which students have more than one advisor?

SQL：
SELECT student.name
FROM student
JOIN advisor ON student.s_ID = advisor.s_ID
GROUP BY student.s_ID
HAVING COUNT(DISTINCT advisor.i_ID) > 1;

---

【示例2】
数据库结构：
course(course_id, title, credits)

自然语言问题：
List all courses that are worth more than 3 credits.

SQL：
SELECT title FROM course WHERE credits > 3;

---

【示例3】
数据库结构：
student(ID,name)
advisor(s_ID, i_ID)

自然语言问题：
What are the names of students who have more than one advisor? 

SQL：
SELECT student.name
FROM student
JOIN advisor ON student.ID = advisor.s_ID
GROUP BY student.ID, student.name
HAVING COUNT(DISTINCT advisor.i_ID) > 1;

---

现在，请根据下面提供的数据库结构和自然语言问题生成 SQL 查询：

数据库结构如下：
{schema}

自然语言问题：
{question}
"""


async def nl_to_sql(question: str, schema: str) -> str:
    """将自然语言问题转换为SQL语句"""
    prompt = PROMPT_TEMPLATE.format(question=question, schema=schema)

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "qwen-turbo",  # 调用千问模型
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "result_format": "message"
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(QWEN_URL, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        return result["output"]["choices"][0]["message"]["content"].strip()