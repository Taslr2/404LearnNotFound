import asyncio
import json
from llm_interface import nl_to_sql  
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich import print 
from rich.table import Table
from rich.console import Console

console = Console()
# MCP 服务配置
server_params = StdioServerParameters(
    command="python",
    args=["main.py"],
    env=None,
)

# 分页设置
PAGE_SIZE = 20  # 每页显示20条记录

async def process_question(question: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print(">> 获取数据库 schema...")
            meta, content = await session.read_resource("mysql://schema")
            text_resource = content[1][0]
            json_str = text_resource.text
            data = json.loads(json_str)
            # print("数据库 schema：")
            # print(json.dumps(data, indent=2, ensure_ascii=False))

            print(">> 使用大模型生成 SQL...")
            sql = await nl_to_sql(question, data)

            print(">> 执行 SQL 查询...")
            result = await session.call_tool("query_data", {"sql": sql})
            content = result.content
            if content and isinstance(content, list):
                first_text_content = content[0]
                json_str = first_text_content.text
                try:
                    data = json.loads(json_str)
                    if data.get("success"):
                        last_results = data.get("results", [])
                        page_index = 0
                        show_page(last_results, page_index, PAGE_SIZE)
                    else:
                        print("❌ 查询失败：", data.get("error"))
                except Exception as e:
                    print("❌ 解析错误:", e)
                    print("原始文本：", json_str)
            else:
                print("返回格式错误")
            # parse_result(result)
            return sql, result

def parse_result(result):
    content = result.content  
    if content and isinstance(content, list):
        first_text_content = content[0]
        json_str = first_text_content.text  # 取出json字符串
        try:
            data = json.loads(json_str)
            #  json.loads 把data字典转成 Python 对象
            print("查询成功？", data.get("success"))
            print("总行数：", data.get("rowCount"))
            print("结果列表示例：")
            for item in data.get("results", []):  
                print(item)
        except Exception as e:
            print("JSON 解析错误:", e)
            print("原始文本：", json_str)
    else:
        print("返回结果格式不符合预期:", content)

def show_page(results, page, page_size=10):
    total = len(results)
    start = page * page_size
    end = min(start + page_size, total)
    print(f"📄 显示第 {start + 1} - {end} 条，共 {total} 条 （第 {page + 1} 页）")
    for item in results[start:end]:
        print(item)
    if end < total:
        print("👉 输入 'next' 查看更多")
    else:
        print("📃 已显示所有数据")
async def fetch_logs():
            try:
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        meta, content = await session.read_resource("mysql://logs")
                        text_resource = content[1][0]
                        logs = json.loads(text_resource.text)
                        print("日志内容如下：")
                        print(json.dumps(logs, indent=2, ensure_ascii=False))
            except Exception as e:
                print("获取日志失败：", e)
def main():
    last_results = []
    page_index = 0
    PAGE_SIZE = 10
    print("输入自然语言问题（输入 'logs' 查看日志，'exit' 退出）")
    while True:
        question = input("请输入查询问题：").strip()
        if question.lower() == "exit":
            print("👋 再见！")
            break

        if question.lower() == "next":
            if last_results:
                page_index += 1
                if page_index * PAGE_SIZE >= len(last_results):
                    print("⚠️ 已经是最后一页，没有更多数据")
                    page_index -= 1  # 不越界
                else:
                    show_page(last_results, page_index, PAGE_SIZE)
            else:
                print("⚠️ 暂无上次查询结果")
            continue

        if question.lower() == "logs":
            asyncio.run(fetch_logs())
            continue

        # 普通查询
        try:
            print(f"\n🔍 正在处理问题：{question}")

            sql, result = asyncio.run(process_question(question))
            print(f"\n✅ 生成的 SQL:\n{sql}")
            parse_result(result)
        except Exception as e:
            print(f"❌ 出错了: {e}\n")

if __name__ == "__main__":
    main()