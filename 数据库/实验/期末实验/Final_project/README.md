# 项目启动说明

欢迎使用本项目！请按照以下步骤完成环境搭建与启动。

---

# 项目依赖说明

本项目基于 Python 开发，使用 MCP 框架构建 MySQL 查询接口，并调用通义千问 API 实现自然语言转 SQL 查询。以下是项目所需的主要依赖及其说明。

---

## 主要依赖列表

| 依赖名称               | 作用                                  | 备注                        |
| ---------------------- | ------------------------------------- | --------------------------- |
| `mcp[cli]>=1.3.0`      | MCP 框架及命令行工具                  | 用于搭建 MCP 服务器的核心库 |
| `mysqlclient>=2.2.7`   | Python 操作 MySQL 的驱动              | 用于数据库连接              |
| `httpx>=0.25.0`        | 异步 HTTP 客户端，用于调用通义千问API | 支持异步网络请求            |
| `python-dotenv>=1.0.0` | 加载 `.env` 配置文件                  | 管理环境变量                |
| `rich>=13.0.0`         | 命令行美化输出                        | 美观打印日志和结果          |

---

## 依赖安装示例

建议在虚拟环境下安装依赖，示例命令：

```bash
uv pip install
```



## 额外说明

在back-end目录下新建`.env` 文件，用于存放数据库连接信息，如下：

```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=yourdatabase
QWEN_API_KEY=sk-55384e91a45d4abb9bd4ce34579bb319
```

- 确保 Python 版本 >= 3.8，支持异步编程。



## 项目运行

进入**back-end**目录下，启动命令：

```bash
uv run main.py
uv run proxy_api.py
```

