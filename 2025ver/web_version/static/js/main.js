// 通用函數庫
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有日期選擇器
    initializeDatepickers();
});

// 初始化所有日期選擇器
function initializeDatepickers() {
    // 獲取所有含有 date 字串的輸入框
    const dateInputs = document.querySelectorAll('input[id*="date"]');
    
    // 設定Flatpickr的通用配置
    const defaultConfig = {
        locale: 'zh_tw',
        dateFormat: 'Y-m-d',
        allowInput: true,
        disableMobile: true, // 在移動設備上也使用自定義選擇器
        monthSelectorType: 'static',
    };
    
    // 為每個輸入框初始化日期選擇器
    dateInputs.forEach(input => {
        flatpickr(input, defaultConfig);
    });
}

// 格式化貨幣顯示
function formatCurrency(amount) {
    return parseFloat(amount).toLocaleString('zh-TW', {
        style: 'currency',
        currency: 'TWD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).replace('NT$', '$ ');
}

// 獲取今天的日期，格式為 YYYY-MM-DD
function getTodayDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}

// 獲取一個月前的日期
function getOneMonthAgoDate() {
    const today = new Date();
    today.setMonth(today.getMonth() - 1);
    
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
}

// 顯示通知消息
function showAlert(message, type = 'success', duration = 3000) {
    // 創建警告元素
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '1050';
    alertDiv.style.maxWidth = '400px';
    
    // 添加消息內容
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // 添加到頁面
    document.body.appendChild(alertDiv);
    
    // 設定自動消失
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => {
            alertDiv.remove();
        }, 150);
    }, duration);
}

// API 錯誤處理
function handleApiError(error) {
    console.error('API Error:', error);
    
    let errorMessage = '發生錯誤，請稍後再試';
    
    if (error.response) {
        // 伺服器返回的錯誤
        try {
            const responseData = error.response.json();
            errorMessage = responseData.error || errorMessage;
        } catch (e) {
            errorMessage = `伺服器錯誤: ${error.response.status}`;
        }
    } else if (error.request) {
        // 沒有收到響應
        errorMessage = '無法連接到伺服器，請檢查網絡連接';
    }
    
    showAlert(errorMessage, 'danger', 5000);
}

// 處理 API 請求
async function apiRequest(url, options = {}) {
    try {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        };
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showAlert(error.message || '請求失敗，請稍後再試', 'danger');
        throw error;
    }
}

// 生成隨機顏色
function generateRandomColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        // 使用HSL以確保顏色飽和度和亮度適中
        const hue = Math.floor(Math.random() * 360);
        colors.push(`hsl(${hue}, 70%, 60%)`);
    }
    return colors;
}

// 下載圖表為圖片
function downloadChart(chart, filename) {
    const link = document.createElement('a');
    link.download = filename;
    link.href = chart.toBase64Image();
    link.click();
}