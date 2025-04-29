-- 連線到 MySQL
mysql -u root -p

-- 建立新資料庫
CREATE DATABASE expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用該資料庫
USE expense_tracker;

-- 建立主要支出記錄表
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 建立類別表
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入預設類別
INSERT INTO categories (name) VALUES 
('飲食'), ('交通'), ('住宿'), ('娛樂'), ('社交'), ('購物'), 
('醫療'), ('日用品'), ('儲值'), ('訂閱'), ('其他');