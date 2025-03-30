import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# 列出系統中所有可用的字型
available_fonts = [f.name for f in fm.fontManager.ttflist]
chinese_fonts = [f for f in available_fonts if any(word in f.lower() for word in ['han', 'ming', 'song', 'kai', 'hei', 'yuan', 'gothic', 'simsum', 'noto', 'cjk'])]
print(chinese_fonts)  # 查看系統中有哪些可能支援中文的字型
# 設定支持中文的字型
mpl.rcParams["font.family"] = "Microsoft YaHei"  # 或其他支援中文的字型
from tkcalendar import DateEntry  # 引入日期選擇器

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳軟體")
        self.root.geometry("800x600")
        
        # 從文件讀取預設品項列表
        self.default_categories = self.load_categories_from_file()
        if not self.default_categories:
            self.default_categories = ["食品", "交通", "住宿", "娛樂", "購物", "醫療", "其他"]
        
        # 存儲記帳數據
        self.expenses = []
        
        # 建立主框架
        self.create_widgets()
    
    def load_categories_from_file(self):
        """從指定文件中讀取類別"""
        categories = []
        categories_file = "categories.txt"  # 類別文件名稱
        
        # 檢查文件是否存在
        if not os.path.exists(categories_file):
            # 創建一個包含預設類別的文件
            try:
                with open(categories_file, 'w', encoding='utf-8') as f:
                    default = ["食品", "交通", "住宿", "娛樂", "購物", "醫療", "其他"]
                    f.write('\n'.join(default))
                categories = default
            except Exception as e:
                print(f"創建類別文件失敗: {e}")
                return []
        else:
            # 從文件讀取類別
            try:
                with open(categories_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        category = line.strip()
                        if category:  # 忽略空行
                            categories.append(category)
            except Exception as e:
                print(f"讀取類別文件失敗: {e}")
                return []
        
        return categories
    
    def save_categories_to_file(self):
        """將當前類別列表儲存到文件"""
        categories_file = "categories.txt"
        try:
            with open(categories_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.default_categories))
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存類別文件失敗: {e}")
        
    def create_widgets(self):
        # 建立主要框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立資料輸入區
        input_frame = ttk.LabelFrame(self.main_frame, text="新增支出", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # 日期選擇器 (使用tkcalendar的DateEntry)
        ttk.Label(input_frame, text="日期:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(input_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 品項選擇及輸入
        ttk.Label(input_frame, text="品項:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.default_categories, width=15)
        self.category_combobox.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 金額輸入
        ttk.Label(input_frame, text="金額:").grid(row=0, column=4, sticky=tk.W, pady=5, padx=(10, 0))
        self.amount_entry = ttk.Entry(input_frame, width=10)
        self.amount_entry.grid(row=0, column=5, sticky=tk.W, pady=5)
        
        # 備註輸入
        ttk.Label(input_frame, text="備註:").grid(row=0, column=6, sticky=tk.W, pady=5, padx=(10, 0))
        self.note_entry = ttk.Entry(input_frame, width=20)
        self.note_entry.grid(row=0, column=7, sticky=tk.W, pady=5)
        
        # 新增按鈕
        add_button = ttk.Button(input_frame, text="新增", command=self.add_expense)
        add_button.grid(row=0, column=8, sticky=tk.E, pady=5, padx=(10, 0))
        
        # 建立資料顯示區
        display_frame = ttk.LabelFrame(self.main_frame, text="支出記錄", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 建立表格
        columns = ("日期", "品項", "金額", "備註")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        
        # 設定列標題
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 添加滾動條
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 建立操作按鈕區
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        edit_button = ttk.Button(buttons_frame, text="修改", command=self.edit_expense)
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(buttons_frame, text="刪除", command=self.delete_expense)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        save_button = ttk.Button(buttons_frame, text="儲存CSV", command=self.save_to_csv)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # 圖像化按鈕區
        visualization_frame = ttk.LabelFrame(self.main_frame, text="數據可視化", padding="10")
        visualization_frame.pack(fill=tk.X, pady=5)
        
        # 按類別統計
        category_stat_button = ttk.Button(visualization_frame, text="類別統計圖", command=lambda: self.show_visualization("category"))
        category_stat_button.pack(side=tk.LEFT, padx=5)
        
        # 按月統計
        monthly_stat_button = ttk.Button(visualization_frame, text="月度統計圖", command=lambda: self.show_visualization("monthly"))
        monthly_stat_button.pack(side=tk.LEFT, padx=5)
        
        # 趨勢分析
        trend_button = ttk.Button(visualization_frame, text="支出趨勢圖", command=lambda: self.show_visualization("trend"))
        trend_button.pack(side=tk.LEFT, padx=5)
        
        # 自定義時間區間統計
        custom_period_button = ttk.Button(visualization_frame, text="自定義區間統計", command=self.custom_period_stat)
        custom_period_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存圖表按鈕
        save_chart_button = ttk.Button(visualization_frame, text="儲存圖表", command=self.save_current_chart)
        save_chart_button.pack(side=tk.LEFT, padx=5)
    
    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get()
        note = self.note_entry.get()
        
        # 基本驗證
        if not date or not category or not amount:
            messagebox.showerror("錯誤", "請填寫日期、品項和金額")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額必須是數字")
            return
        
        # 新增到記錄中
        expense_data = {"日期": date, "品項": category, "金額": amount, "備註": note}
        self.expenses.append(expense_data)
        
        # 更新表格
        self.tree.insert("", tk.END, values=(date, category, amount, note))
        
        # 清空輸入欄位
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        
        # 如果輸入了自定義類別，添加到下拉列表並更新文件
        if category not in self.default_categories and category:
            self.default_categories.append(category)
            self.category_combobox.configure(values=self.default_categories)
            self.save_categories_to_file()  # 更新類別文件

    def edit_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("錯誤", "請選擇要修改的項目")
            return
        
        selected_index = self.tree.index(selected_item[0])
        expense = self.expenses[selected_index]
        
        # 創建修改視窗
        edit_window = tk.Toplevel(self.root)
        edit_window.title("修改支出")
        edit_window.geometry("400x150")
        
        # 日期 (使用DateEntry)
        ttk.Label(edit_window, text="日期:").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(edit_window, width=12, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        # 設定當前日期
        try:
            current_date = datetime.strptime(expense["日期"], "%Y-%m-%d").date()
            date_entry.set_date(current_date)
        except ValueError:
            # 如果日期格式不正確，使用今天的日期
            date_entry.set_date(datetime.now().date())
        
        # 品項
        ttk.Label(edit_window, text="品項:").grid(row=1, column=0, padx=5, pady=5)
        category_var = tk.StringVar(value=expense["品項"])
        category_combobox = ttk.Combobox(edit_window, textvariable=category_var, values=self.default_categories)
        category_combobox.grid(row=1, column=1, padx=5, pady=5)
        
        # 金額
        ttk.Label(edit_window, text="金額:").grid(row=2, column=0, padx=5, pady=5)
        amount_entry = ttk.Entry(edit_window)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        amount_entry.insert(0, expense["金額"])
        
        # 備註
        ttk.Label(edit_window, text="備註:").grid(row=0, column=2, padx=5, pady=5)
        note_entry = ttk.Entry(edit_window, width=20)
        note_entry.grid(row=0, column=3, padx=5, pady=5)
        note_entry.insert(0, expense["備註"])
        
        # 儲存修改按鈕
        def save_edit():
            date = date_entry.get()
            category = category_var.get()
            amount_str = amount_entry.get()
            note = note_entry.get()
            
            # 基本驗證
            if not date or not category or not amount_str:
                messagebox.showerror("錯誤", "請填寫日期、品項和金額", parent=edit_window)
                return
            
            try:
                amount = float(amount_str)
            except ValueError:
                messagebox.showerror("錯誤", "金額必須是數字", parent=edit_window)
                return
            
            # 更新數據
            self.expenses[selected_index] = {"日期": date, "品項": category, "金額": amount, "備註": note}
            self.tree.item(selected_item[0], values=(date, category, amount, note))
            
            # 如果修改了品項，並且是新的品項，添加到預設列表
            if category not in self.default_categories and category:
                self.default_categories.append(category)
                self.category_combobox.configure(values=self.default_categories)
                self.save_categories_to_file()  # 更新類別文件
            
            edit_window.destroy()
        
        save_button = ttk.Button(edit_window, text="儲存", command=save_edit)
        save_button.grid(row=3, column=1, padx=5, pady=10)
        
    def delete_expense(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("錯誤", "請選擇要刪除的項目")
            return
        
        # 確認刪除
        confirm = messagebox.askyesno("確認", "確定要刪除選擇的項目嗎？")
        if not confirm:
            return
        
        # 刪除項目
        selected_index = self.tree.index(selected_item[0])
        self.expenses.pop(selected_index)
        self.tree.delete(selected_item)
    
    def save_to_csv(self):
        if not self.expenses:
            messagebox.showerror("錯誤", "沒有數據可以儲存")
            return
        
        # 選擇儲存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=["日期", "品項", "金額", "備註"])
                writer.writeheader()
                writer.writerows(self.expenses)
            
            messagebox.showinfo("成功", f"數據已儲存至 {file_path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存失敗: {e}")
    
    def show_visualization(self, chart_type):
        if not self.expenses:
            messagebox.showerror("錯誤", "沒有數據可以視覺化")
            return
        
        # 創建視覺化視窗
        viz_window = tk.Toplevel(self.root)
        viz_window.title("支出視覺化")
        viz_window.geometry("800x600")
        
        # 轉換數據為 DataFrame
        df = pd.DataFrame(self.expenses)
        df["金額"] = pd.to_numeric(df["金額"])
        
        # 確保日期只精確到"年-月-日"，不含時間
        df["日期"] = pd.to_datetime(df["日期"]).dt.date
        
        # 創建圖表
        fig, ax = plt.subplots(figsize=(10, 6))
        self.current_fig = fig  # 儲存當前圖表以便儲存
        
        if chart_type == "category":
            # 按類別統計
            category_data = df.groupby("品項")["金額"].sum()
            category_data.plot(kind="pie", ax=ax, autopct='%1.1f%%')
            ax.set_title("各類別支出佔比")
            ax.set_ylabel("")
            
        elif chart_type == "monthly":
            # 按月份統計，但保持日期格式為"年-月-日"
            df["月份"] = pd.to_datetime(df["日期"]).dt.strftime("%Y-%m")
            monthly_data = df.groupby("月份")["金額"].sum()
            monthly_data.plot(kind="bar", ax=ax)
            ax.set_title("月度支出統計")
            ax.set_xlabel("月份")
            ax.set_ylabel("金額")
            
        elif chart_type == "trend":
            # 支出趨勢，確保日期只顯示到日
            daily_sum = df.groupby("日期")["金額"].sum().reset_index()
            daily_sum = daily_sum.sort_values("日期")
            date_strings = [str(d) for d in daily_sum["日期"]]
            ax.plot(date_strings, daily_sum["金額"], marker='o')
            ax.set_title("支出趨勢圖")
            ax.set_xlabel("日期")
            ax.set_ylabel("金額")
            
            # 調整 x 軸標籤角度，避免重疊
            plt.xticks(rotation=45)
            plt.tight_layout()
        
        # 嵌入圖表到視窗
        canvas = FigureCanvasTkAgg(fig, master=viz_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def custom_period_stat(self):
        if not self.expenses:
            messagebox.showerror("錯誤", "沒有數據可以分析")
            return
        
        # 創建自定義時間區間視窗
        period_window = tk.Toplevel(self.root)
        period_window.title("自定義時間區間")
        period_window.geometry("350x150")
        
        ttk.Label(period_window, text="開始日期:").grid(row=0, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(period_window, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(period_window, text="結束日期:").grid(row=1, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(period_window, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        end_date_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def show_custom_stat():
            start_date = start_date_entry.get_date()
            end_date = end_date_entry.get_date()
            
            # 轉換並過濾數據
            df = pd.DataFrame(self.expenses)
            df["金額"] = pd.to_numeric(df["金額"])
            
            # 轉換日期並確保它只精確到日期
            df["日期"] = pd.to_datetime(df["日期"]).dt.date
            
            # 過濾日期範圍
            mask = (df["日期"] >= start_date) & (df["日期"] <= end_date)
            filtered_df = df.loc[mask]
            
            if filtered_df.empty:
                messagebox.showerror("錯誤", "選擇的日期範圍內沒有數據", parent=period_window)
                return
            
            period_window.destroy()
            
            # 創建視覺化視窗
            viz_window = tk.Toplevel(self.root)
            viz_window.title(f"自定義區間統計 ({start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')})")
            viz_window.geometry("800x600")
            
            # 創建圖表
            fig = plt.figure(figsize=(12, 8))
            self.current_fig = fig
            
            # 子圖1: 類別佔比
            ax1 = fig.add_subplot(221)
            category_data = filtered_df.groupby("品項")["金額"].sum()
            category_data.plot(kind="pie", ax=ax1, autopct='%1.1f%%')
            ax1.set_title("類別佔比")
            ax1.set_ylabel("")
            
            # 子圖2: 每日支出
            ax2 = fig.add_subplot(222)
            
            # 轉換日期為字符串，確保只顯示到日期
            daily_data = filtered_df.groupby("日期")["金額"].sum().reset_index()
            daily_data = daily_data.sort_values("日期")
            date_strings = [str(d) for d in daily_data["日期"]]
            daily_sums = daily_data["金額"].values
            
            # 繪製柱狀圖
            ax2.bar(date_strings, daily_sums)
            ax2.set_title("每日支出")
            ax2.set_xlabel("日期")
            ax2.set_ylabel("金額")
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            ax2.tick_params(axis='x', labelsize=8)  # 調整標籤大小
            
            # 子圖3: 總覽統計文字
            ax3 = fig.add_subplot(212)
            ax3.axis('off')
            total_amount = filtered_df["金額"].sum()
            avg_amount = filtered_df["金額"].mean()
            max_amount = filtered_df["金額"].max()
            min_amount = filtered_df["金額"].min()
            
            stats_text = (
                f"統計期間: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}\n"
                f"總支出: {total_amount:.2f}\n"
                f"平均每日支出: {avg_amount:.2f}\n"
                f"最高單筆支出: {max_amount:.2f}\n"
                f"最低單筆支出: {min_amount:.2f}\n"
                f"記錄筆數: {len(filtered_df)}\n"
                f"消費種類數: {len(category_data)}"
            )
            
            ax3.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center')
            
            # 調整布局，確保標籤不被切掉
            plt.tight_layout()
            
            # 嵌入圖表到視窗
            canvas = FigureCanvasTkAgg(fig, master=viz_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        analyze_button = ttk.Button(period_window, text="分析", command=show_custom_stat)
        analyze_button.grid(row=2, column=0, columnspan=2, pady=15)
    
    def save_current_chart(self):
        if not hasattr(self, 'current_fig'):
            messagebox.showerror("錯誤", "沒有圖表可儲存")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.current_fig.savefig(file_path)
            messagebox.showinfo("成功", f"圖表已儲存至 {file_path}")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存失敗: {e}")

def load_from_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if not file_path:
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        messagebox.showerror("錯誤", f"載入失敗: {e}")
        return []

def main():
    root = tk.Tk()
    app = ExpenseTracker(root)
    
    # 檢查是否要載入現有數據
    load_data = messagebox.askyesno("載入數據", "是否要從CSV檔載入既有數據？")
    if load_data:
        expenses = load_from_csv()
        for expense in expenses:
            app.expenses.append(expense)
            app.tree.insert("", tk.END, values=(
                expense["日期"], 
                expense["品項"], 
                expense["金額"], 
                expense.get("備註", "")
            ))
    
    root.mainloop()

if __name__ == "__main__":
    main()