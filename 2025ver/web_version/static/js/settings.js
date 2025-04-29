// 設定頁面 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 初始化日期選擇器
    initializeDatepickers();
    
    // 設定默認匯出日期範圍：最近一個月
    document.getElementById('export-start-date').value = getOneMonthAgoDate();
    document.getElementById('export-end-date').value = getTodayDate();
    
    // 初始化事件監聽器
    initEventListeners();
});

// 初始化事件監聽器
function initEventListeners() {
    // 添加類別表單
    document.getElementById('add-category-form').addEventListener('submit', handleAddCategory);
    
    // 刪除類別按鈕
    document.querySelectorAll('.delete-category').forEach(button => {
        button.addEventListener('click', function() {
            openDeleteCategoryModal(this.dataset.id);
        });
    });
    
    // 確認刪除類別按鈕
    document.getElementById('confirm-delete-category-btn').addEventListener('click', handleDeleteCategory);
    
    // 匯出 CSV 按鈕
    document.getElementById('export-csv-btn').addEventListener('click', handleExportCSV);
}

// 處理添加類別
async function handleAddCategory(event) {
    event.preventDefault();
    
    const categoryName = document.getElementById('new-category').value.trim();
    
    if (!categoryName) {
        showAlert('請輸入類別名稱', 'warning');
        return;
    }
    
    try {
        const response = await apiRequest('/api/categories', {
            method: 'POST',
            body: JSON.stringify({ name: categoryName })
        });
        
        // 添加新類別到表格
        const tableBody = document.getElementById('categories-table');
        const newRow = document.createElement('tr');
        
        newRow.innerHTML = `
            <td>${response.name}</td>
            <td>
                <button class="btn btn-sm btn-danger delete-category" data-id="${response.id}">刪除</button>
            </td>
        `;
        
        // 添加刪除按鈕的事件監聽器
        newRow.querySelector('.delete-category').addEventListener('click', function() {
            openDeleteCategoryModal(this.dataset.id);
        });
        
        tableBody.appendChild(newRow);
        
        // 清空輸入框
        document.getElementById('new-category').value = '';
        
        showAlert('類別已成功添加！');
    } catch (error) {
        console.error('添加類別時發生錯誤:', error);
    }
}

// 開啟刪除類別確認模態框
function openDeleteCategoryModal(categoryId) {
    document.getElementById('delete-category-id').value = categoryId;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteCategoryModal'));
    modal.show();
}

// 處理刪除類別
async function handleDeleteCategory() {
    const categoryId = document.getElementById('delete-category-id').value;
    
    try {
        await apiRequest(`/api/categories/${categoryId}`, {
            method: 'DELETE'
        });
        
        // 關閉模態框
        bootstrap.Modal.getInstance(document.getElementById('deleteCategoryModal')).hide();
        
        // 從表格中移除該類別
        const categoryElement = document.querySelector(`.delete-category[data-id="${categoryId}"]`).closest('tr');
        categoryElement.remove();
        
        showAlert('類別已成功刪除！');
    } catch (error) {
        console.error('刪除類別時發生錯誤:', error);
        
        // 如果錯誤是因為該類別正在使用中
        if (error.message && error.message.includes('已被使用')) {
            showAlert('無法刪除：此類別已被使用。請先修改或刪除使用此類別的支出記錄。', 'warning');
        }
    }
}

// 處理匯出 CSV
async function handleExportCSV() {
    const startDate = document.getElementById('export-start-date').value;
    const endDate = document.getElementById('export-end-date').value;
    
    if (!startDate || !endDate) {
        showAlert('請選擇開始和結束日期', 'warning');
        return;
    }
    
    try {
        // 獲取指定日期範圍的支出資料
        let url = `/api/expenses?start_date=${startDate}&end_date=${endDate}`;
        const expenses = await apiRequest(url);
        
        if (expenses.length === 0) {
            showAlert('所選日期範圍內沒有支出記錄', 'warning');
            return;
        }
        
        // 生成 CSV 內容
        let csvContent = "日期,品項,金額,備註\n";
        
        expenses.forEach(expense => {
            const note = expense.note ? `"${expense.note}"` : "";
            csvContent += `${expense.date},${expense.category},${expense.amount},${note}\n`;
        });
        
        // 將 CSV 內容轉為 Blob
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        
        // 建立下載連結
        const link = document.createElement('a');
        const filename = `支出記錄_${startDate}_至_${endDate}.csv`;
        
        if (navigator.msSaveBlob) {
            // 支援 IE10+
            navigator.msSaveBlob(blob, filename);
        } else {
            // 其他現代瀏覽器
            const url = URL.createObjectURL(blob);
            link.href = url;
            link.download = filename;
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            
            setTimeout(() => {
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
            }, 100);
        }
        
        showAlert('CSV 檔案已成功匯出！');
    } catch (error) {
        console.error('匯出 CSV 時發生錯誤:', error);
        showAlert('匯出 CSV 時發生錯誤', 'danger');
    }
}