// 主頁 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // 初始化日期輸入框為今天的日期
    document.getElementById('date').value = getTodayDate();
    
    // 初始化事件監聽器
    initEventListeners();
    
    // 載入支出記錄
    loadExpenses();
});

// 初始化所有事件監聽器
function initEventListeners() {
    // 新增支出表單提交
    document.getElementById('expense-form').addEventListener('submit', handleAddExpense);
    
    // 修改支出按鈕
    document.getElementById('save-edit-btn').addEventListener('click', handleEditExpense);
    
    // 確認刪除按鈕
    document.getElementById('confirm-delete-btn').addEventListener('click', handleDeleteExpense);
    
    // 篩選按鈕
    document.getElementById('filter-btn').addEventListener('click', handleFilterExpenses);
    
    // 重設篩選按鈕
    document.getElementById('reset-filter-btn').addEventListener('click', resetFilter);
}

// 載入支出記錄
async function loadExpenses(startDate = null, endDate = null) {
    try {
        let url = '/api/expenses';
        
        // 添加日期範圍篩選參數
        if (startDate && endDate) {
            url += `?start_date=${startDate}&end_date=${endDate}`;
        }
        
        const expenses = await apiRequest(url);
        displayExpenses(expenses);
    } catch (error) {
        console.error('載入支出記錄時發生錯誤:', error);
    }
}

// 顯示支出記錄
function displayExpenses(expenses) {
    const tableBody = document.getElementById('expenses-table');
    const noDataMessage = document.getElementById('no-data-message');
    
    // 清空表格
    tableBody.innerHTML = '';
    
    if (expenses.length === 0) {
        // 沒有數據時顯示提示信息
        noDataMessage.classList.remove('d-none');
        return;
    }
    
    // 有數據時隱藏提示信息
    noDataMessage.classList.add('d-none');
    
    // 填充表格
    expenses.forEach(expense => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${expense.date}</td>
            <td>${expense.category}</td>
            <td>${formatCurrency(expense.amount)}</td>
            <td>${expense.note || ''}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${expense.id}">修改</button>
                <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${expense.id}">刪除</button>
            </td>
        `;
        
        // 添加修改按鈕點擊事件
        row.querySelector('.edit-btn').addEventListener('click', () => openEditModal(expense));
        
        // 添加刪除按鈕點擊事件
        row.querySelector('.delete-btn').addEventListener('click', () => openDeleteModal(expense.id));
        
        tableBody.appendChild(row);
    });
}

// 處理新增支出
async function handleAddExpense(event) {
    event.preventDefault();
    
    const formData = {
        date: document.getElementById('date').value,
        category: document.getElementById('category').value,
        amount: parseFloat(document.getElementById('amount').value),
        note: document.getElementById('note').value
    };
    
    try {
        await apiRequest('/api/expenses', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        // 重設表單金額和備註
        document.getElementById('amount').value = '';
        document.getElementById('note').value = '';
        
        // 重新載入支出記錄
        loadExpenses(
            document.getElementById('filter-start-date').value,
            document.getElementById('filter-end-date').value
        );
        
        showAlert('支出已成功新增！');
    } catch (error) {
        console.error('新增支出時發生錯誤:', error);
    }
}

// 開啟修改支出模態框
function openEditModal(expense) {
    // 設置模態框的值
    document.getElementById('edit-id').value = expense.id;
    document.getElementById('edit-date').value = expense.date;
    document.getElementById('edit-category').value = expense.category;
    document.getElementById('edit-amount').value = expense.amount;
    document.getElementById('edit-note').value = expense.note || '';
    
    // 顯示模態框
    const modal = new bootstrap.Modal(document.getElementById('editExpenseModal'));
    modal.show();
}

// 處理修改支出
async function handleEditExpense() {
    const expenseId = document.getElementById('edit-id').value;
    
    const formData = {
        date: document.getElementById('edit-date').value,
        category: document.getElementById('edit-category').value,
        amount: parseFloat(document.getElementById('edit-amount').value),
        note: document.getElementById('edit-note').value
    };
    
    try {
        await apiRequest(`/api/expenses/${expenseId}`, {
            method: 'PUT',
            body: JSON.stringify(formData)
        });
        
        // 關閉模態框
        bootstrap.Modal.getInstance(document.getElementById('editExpenseModal')).hide();
        
        // 重新載入支出記錄
        loadExpenses(
            document.getElementById('filter-start-date').value,
            document.getElementById('filter-end-date').value
        );
        
        showAlert('支出已成功修改！');
    } catch (error) {
        console.error('修改支出時發生錯誤:', error);
    }
}

// 開啟刪除確認模態框
function openDeleteModal(expenseId) {
    document.getElementById('delete-id').value = expenseId;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteExpenseModal'));
    modal.show();
}

// 處理刪除支出
async function handleDeleteExpense() {
    const expenseId = document.getElementById('delete-id').value;
    
    try {
        await apiRequest(`/api/expenses/${expenseId}`, {
            method: 'DELETE'
        });
        
        // 關閉模態框
        bootstrap.Modal.getInstance(document.getElementById('deleteExpenseModal')).hide();
        
        // 重新載入支出記錄
        loadExpenses(
            document.getElementById('filter-start-date').value,
            document.getElementById('filter-end-date').value
        );
        
        showAlert('支出已成功刪除！');
    } catch (error) {
        console.error('刪除支出時發生錯誤:', error);
    }
}

// 處理篩選支出
function handleFilterExpenses() {
    const startDate = document.getElementById('filter-start-date').value;
    const endDate = document.getElementById('filter-end-date').value;
    
    if (!startDate || !endDate) {
        showAlert('請選擇開始和結束日期', 'warning');
        return;
    }
    
    loadExpenses(startDate, endDate);
}

// 重設篩選
function resetFilter() {
    document.getElementById('filter-start-date').value = '';
    document.getElementById('filter-end-date').value = '';
    
    loadExpenses();
}