import pandas as pd
import mysql.connector
import csv
from datetime import datetime

# 資料庫連線設定
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 's87315teve',  # 請替換為你的 MySQL 密碼
    'database': 'expense_tracker'
}

# 連線到資料庫
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 讀取 CSV 檔案
try:
    with open('money.csv', 'r', encoding='utf-8-sig') as file:
        df = pd.read_csv(file)
        
    # 確保日期格式正確
    df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
    
    # 插入資料
    for index, row in df.iterrows():
        # 檢查類別是否存在，若不存在則新增
        cursor.execute("SELECT id FROM categories WHERE name = %s", (row['品項'],))
        category_result = cursor.fetchone()
        
        if not category_result:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (row['品項'],))
            conn.commit()
        
        # 插入支出記錄
        sql = "INSERT INTO expenses (date, category, amount, note) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (row['日期'], row['品項'], float(row['金額']), row.get('備註', '')))
    
    conn.commit()
    print(f"成功匯入 {len(df)} 筆資料")

except Exception as e:
    print(f"匯入資料時發生錯誤: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()