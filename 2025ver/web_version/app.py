from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
from datetime import datetime, timedelta
import json
import calendar
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 資料庫連線函數
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn, conn.cursor(dictionary=True)

# 主頁 - 記帳界面
@app.route('/')
def index():
    # 獲取類別列表
    conn, cursor = get_db_connection()
    cursor.execute("SELECT name FROM categories ORDER BY name")
    categories = [row['name'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return render_template('index.html', categories=categories)

# API 端點 - 獲取所有支出記錄
@app.route('/api/expenses')
def get_expenses():
    conn, cursor = get_db_connection()
    
    # 支援日期範圍過濾
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        cursor.execute(
            "SELECT id, date, category, amount, note FROM expenses WHERE date BETWEEN %s AND %s ORDER BY date DESC",
            (start_date, end_date)
        )
    else:
        cursor.execute("SELECT id, date, category, amount, note FROM expenses ORDER BY date DESC")
    
    expenses = []
    for row in cursor.fetchall():
        row['date'] = row['date'].strftime('%Y-%m-%d')
        expenses.append(row)
    
    cursor.close()
    conn.close()
    return jsonify(expenses)

# API 端點 - 添加新支出
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    
    conn, cursor = get_db_connection()
    try:
        # 檢查類別是否存在，不存在則添加
        cursor.execute("SELECT id FROM categories WHERE name = %s", (data['category'],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (data['category'],))
        
        # 添加支出記錄
        cursor.execute(
            "INSERT INTO expenses (date, category, amount, note) VALUES (%s, %s, %s, %s)",
            (data['date'], data['category'], data['amount'], data.get('note', ''))
        )
        
        new_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        flash('支出已成功添加！', 'success')
        return jsonify({"success": True, "id": new_id})
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

# API 端點 - 更新支出
@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    
    conn, cursor = get_db_connection()
    try:
        # 檢查類別是否存在，不存在則添加
        cursor.execute("SELECT id FROM categories WHERE name = %s", (data['category'],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (data['category'],))
        
        # 更新支出記錄
        cursor.execute(
            "UPDATE expenses SET date = %s, category = %s, amount = %s, note = %s WHERE id = %s",
            (data['date'], data['category'], data['amount'], data.get('note', ''), expense_id)
        )
        
        cursor.close()
        conn.close()
        
        flash('支出已成功更新！', 'success')
        return jsonify({"success": True})
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

# API 端點 - 刪除支出
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        
        cursor.close()
        conn.close()
        
        flash('支出已成功刪除！', 'success')
        return jsonify({"success": True})
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

# 統計分析頁面
@app.route('/stats')
def stats():
    return render_template('stats.html')

# API 端點 - 按類別統計
@app.route('/api/stats/by-category')
def stats_by_category():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn, cursor = get_db_connection()
    
    if start_date and end_date:
        cursor.execute("""
            SELECT category, SUM(amount) as total 
            FROM expenses 
            WHERE date BETWEEN %s AND %s 
            GROUP BY category 
            ORDER BY total DESC
        """, (start_date, end_date))
    else:
        cursor.execute("""
            SELECT category, SUM(amount) as total 
            FROM expenses 
            GROUP BY category 
            ORDER BY total DESC
        """)
    
    categories_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(categories_data)

# API 端點 - 按月份統計
@app.route('/api/stats/by-month')
def stats_by_month():
    conn, cursor = get_db_connection()
    
    cursor.execute("""
        SELECT DATE_FORMAT(date, '%Y-%m') as month, SUM(amount) as total 
        FROM expenses 
        GROUP BY month 
        ORDER BY month
    """)
    
    monthly_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(monthly_data)

# API 端點 - 支出趨勢
@app.route('/api/stats/trend')
def stats_trend():
    days = int(request.args.get('days', 30))
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    conn, cursor = get_db_connection()
    
    cursor.execute("""
        SELECT date, SUM(amount) as total 
        FROM expenses 
        WHERE date BETWEEN %s AND %s 
        GROUP BY date 
        ORDER BY date
    """, (start_date, end_date))
    
    trend_data = []
    for row in cursor.fetchall():
        trend_data.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'total': float(row['total'])
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(trend_data)

# 設定頁面 - 管理類別
@app.route('/settings')
def settings():
    conn, cursor = get_db_connection()
    cursor.execute("SELECT id, name FROM categories ORDER BY name")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('settings.html', categories=categories)

# API 端點 - 添加類別
@app.route('/api/categories', methods=['POST'])
def add_category():
    data = request.json
    category_name = data.get('name', '').strip()
    
    if not category_name:
        return jsonify({"success": False, "error": "類別名稱不能為空"}), 400
    
    conn, cursor = get_db_connection()
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
        new_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        flash('類別已成功添加！', 'success')
        return jsonify({"success": True, "id": new_id, "name": category_name})
    
    except mysql.connector.IntegrityError:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": "此類別已存在"}), 400
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

# API 端點 - 刪除類別
@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    conn, cursor = get_db_connection()
    
    try:
        # 先檢查是否有使用此類別的支出
        cursor.execute("SELECT COUNT(*) as count FROM expenses WHERE category = (SELECT name FROM categories WHERE id = %s)", (category_id,))
        result = cursor.fetchone()
        
        if result['count'] > 0:
            cursor.close()
            conn.close()
            return jsonify({
                "success": False, 
                "error": "此類別已被使用，無法刪除。請先修改或刪除使用此類別的支出記錄。"
            }), 400
        
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        
        cursor.close()
        conn.close()
        
        flash('類別已成功刪除！', 'success')
        return jsonify({"success": True})
    
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)