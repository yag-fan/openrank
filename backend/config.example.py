import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置（对接Top300仓库日志数据库）
# 请复制此文件为 config.py 并填入你的数据库配置
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "your_username",
    "password": "your_password",
    "db": "your_database",
    "port": 3306,
    "charset": "utf8mb4"
}

# Flask配置
FLASK_CONFIG = {
    "DEBUG": True,
    "JSON_AS_ASCII": False  # 支持中文
}

