import mysql.connector
import pandas as pd
import sys
import os
from getpass import getpass
from datetime import datetime

def create_database(host, user, password, db_name):
    """創建資料庫和必要的表格"""
    print(f"正在連接到 MySQL 伺服器...")
    
    # 連接到 MySQL
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        print(f"成功連接到 MySQL 伺服器！")
        
        # 建立資料庫
        print(f"正在建立資料庫 '{db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"資料庫 '{db_name}' 已建立！")
        
        # 使用新建立的資料庫
        cursor.execute(f"USE {db_name}")
        
        # 建立支出表
        print("正在建立 'expenses' 表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("'expenses' 表已建立！")
        
        # 建立類別表
        print("正在建立 'categories' 表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("'categories' 表已建立！")
        
        return conn, cursor
    except mysql.connector.Error as e:
        print(f"資料庫建立錯誤: {e}")
        sys.exit(1)

def import_categories(cursor, categories_file):
    """從檔案匯入類別"""
    if not os.path.exists(categories_file):
        print(f"警告: 類別檔案 '{categories_file}' 不存在")
        return
    
    print(f"正在從 '{categories_file}' 匯入類別...")
    
    try:
        with open(categories_file, 'r', encoding='utf-8') as f:
            categories = [line.strip() for line in f.readlines() if line.strip()]
        
        for category in categories:
            try:
                cursor.execute("INSERT IGNORE INTO categories (name) VALUES (%s)", (category,))
                print(f"  已新增類別: {category}")
            except mysql.connector.Error as e:
                print(f"  新增類別 '{category}' 時發生錯誤: {e}")
        
        print(f"類別匯入完成！")
    except Exception as e:
        print(f"類別匯入錯誤: {e}")

def import_expenses(cursor, csv_file):
    """從 CSV 檔案匯入支出記錄"""
    if not os.path.exists(csv_file):
        print(f"警告: 支出記錄檔案 '{csv_file}' 不存在")
        return
    
    print(f"正在從 '{csv_file}' 匯入支出記錄...")
    
    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        
        # 檢查所需欄位是否存在
        required_columns = ['日期', '品項', '金額']
        for col in required_columns:
            if col not in df.columns:
                print(f"錯誤: CSV 檔案中缺少必要欄位 '{col}'")
                return
        
        # 確保日期格式正確
        df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
        
        # 如果沒有備註欄位，添加空備註
        if '備註' not in df.columns:
            df['備註'] = ''
        
        total_rows = len(df)
        success_count = 0
        error_count = 0
        
        # 插入每筆支出記錄
        for index, row in df.iterrows():
            try:
                # 確保類別存在
                cursor.execute("SELECT id FROM categories WHERE name = %s", (row['品項'],))
                result = cursor.fetchone()
                
                if not result:
                    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (row['品項'],))
                
                # 插入支出記錄
                cursor.execute(
                    "INSERT INTO expenses (date, category, amount, note) VALUES (%s, %s, %s, %s)",
                    (row['日期'], row['品項'], float(row['金額']), row.get('備註', ''))
                )
                success_count += 1
                
                # 顯示進度
                if index % 10 == 0 or index == total_rows - 1:
                    print(f"  進度: {index + 1}/{total_rows} ({round((index + 1) / total_rows * 100, 1)}%)")
                
            except Exception as e:
                print(f"  插入第 {index + 1} 筆記錄時發生錯誤: {e}")
                error_count += 1
        
        print(f"支出記錄匯入完成！成功: {success_count}, 失敗: {error_count}")
    except Exception as e:
        print(f"支出記錄匯入錯誤: {e}")

def setup_config_file(host, user, password, db_name):
    """設定配置文件"""
    print("正在創建配置文件...")
    
    config_content = f"""# 資料庫配置
DB_CONFIG = {{
    'host': '{host}',
    'user': '{user}',
    'password': '{password}',
    'database': '{db_name}'
}}

# Flask 配置
SECRET_KEY = '{os.urandom(24).hex()}'
"""
    
    try:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("配置文件 'config.py' 已創建！")
    except Exception as e:
        print(f"創建配置文件時發生錯誤: {e}")

def main():
    print("\n===== 記帳軟體網頁版設置 =====\n")
    
    # 獲取用戶輸入
    host = input("MySQL 主機地址 [localhost]: ") or "localhost"
    user = input("MySQL 用戶名 [root]: ") or "root"
    password = getpass("MySQL 密碼: ")
    db_name = input("資料庫名稱 [expense_tracker]: ") or "expense_tracker"
    
    # 建立資料庫
    conn, cursor = create_database(host, user, password, db_name)
    
    # 設定配置文件
    setup_config_file(host, user, password, db_name)
    
    # 匯入類別
    categories_file = input("\n類別文件路徑 [categories.txt]: ") or "categories.txt"
    import_categories(cursor, categories_file)
    
    # 匯入 CSV
    csv_file = input("\nCSV 檔案路徑 [money.csv]: ") or "money.csv"
    import_expenses(cursor, csv_file)
    
    # 提交所有更改
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n===== 設置完成 =====")
    print("您可以使用以下命令啟動網頁應用程式：")
    print("  flask run")
    print("或")
    print("  python app.py")

if __name__ == "__main__":
    main()