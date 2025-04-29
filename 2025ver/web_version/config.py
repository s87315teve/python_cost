import os
# 資料庫配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 's87315teve',  # 請替換為你的 MySQL 密碼
    'database': 'expense_tracker'
}

# Flask 配置
SECRET_KEY = os.urandom(24).hex()  # 可以使用 os.urandom(24).hex() 生成