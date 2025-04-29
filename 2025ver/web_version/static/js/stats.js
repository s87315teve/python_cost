// 統計分析頁面 JavaScript
let categoryChart, monthlyChart, trendChart;
let currentTrendPeriod = 30;

document.addEventListener('DOMContentLoaded', function() {
    // 初始化日期選擇器
    initializeDatepickers();
    
    // 設定默認日期範圍：最近一個月
    document.getElementById('stats-start-date').value = getOneMonthAgoDate();
    document.getElementById('stats-end-date').value = getTodayDate();
    
    // 初始化事件監聽器
    initEventListeners();
    
    // 載入初始統計數據
    loadStatistics();
});

// 初始化事件監聽器
function initEventListeners() {
    // 統計分析按鈕
    document.getElementById('stats-filter-btn').addEventListener('click', handleFilterStats);
    
    // 趨勢圖時間範圍按鈕
    document.querySelectorAll('.trend-period').forEach(button => {
        button.addEventListener('click', function() {
            // 移除所有按鈕的 active 類別
            document.querySelectorAll('.trend-period').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // 為當前按鈕添加 active 類別
            this.classList.add('active');
            
            // 獲取並設置趨勢圖的天數
            currentTrendPeriod = parseInt(this.dataset.days);
            
            // 更新趨勢圖
            loadTrendData(currentTrendPeriod);
        });
    });
    
    // 下載圖表按鈕
    document.getElementById('download-charts').addEventListener('click', downloadAllCharts);
}

// 載入統計數據
async function loadStatistics() {
    const startDate = document.getElementById('stats-start-date').value;
    const endDate = document.getElementById('stats-end-date').value;
    
    // 檢查日期是否有效
    if (startDate && endDate) {
        try {
            // 同時載入各項統計資料
            await Promise.all([
                loadCategoryData(startDate, endDate),
                loadMonthlyData(),
                loadTrendData(currentTrendPeriod),
                loadSummaryData(startDate, endDate)
            ]);
        } catch (error) {
            console.error('載入統計數據時發生錯誤:', error);
        }
    } else {
        showAlert('請選擇有效的日期範圍', 'warning');
    }
}

// 載入類別統計資料
async function loadCategoryData(startDate, endDate) {
    try {
        let url = '/api/stats/by-category';
        
        if (startDate && endDate) {
            url += `?start_date=${startDate}&end_date=${endDate}`;
        }
        
        const data = await apiRequest(url);
        
        if (data.length === 0) {
            document.getElementById('no-category-data').classList.remove('d-none');
            if (categoryChart) {
                categoryChart.destroy();
                categoryChart = null;
            }
            return;
        }
        
        document.getElementById('no-category-data').classList.add('d-none');
        
        // 準備圖表資料
        const labels = data.map(item => item.category);
        const values = data.map(item => item.total);
        const backgroundColors = generateRandomColors(data.length);
        
        // 創建或更新圖表
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        if (categoryChart) {
            categoryChart.data.labels = labels;
            categoryChart.data.datasets[0].data = values;
            categoryChart.data.datasets[0].backgroundColor = backgroundColors;
            categoryChart.update();
        } else {
            categoryChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: backgroundColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw;
                                    const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${formatCurrency(value)} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('載入類別統計資料時發生錯誤:', error);
    }
}

// 載入月度統計資料
async function loadMonthlyData() {
    try {
        const data = await apiRequest('/api/stats/by-month');
        
        if (data.length === 0) {
            document.getElementById('no-monthly-data').classList.remove('d-none');
            if (monthlyChart) {
                monthlyChart.destroy();
                monthlyChart = null;
            }
            return;
        }
        
        document.getElementById('no-monthly-data').classList.add('d-none');
        
        // 準備圖表資料
        const labels = data.map(item => item.month);
        const values = data.map(item => item.total);
        
        // 創建或更新圖表
        const ctx = document.getElementById('monthlyChart').getContext('2d');
        
        if (monthlyChart) {
            monthlyChart.data.labels = labels;
            monthlyChart.data.datasets[0].data = values;
            monthlyChart.update();
        } else {
            monthlyChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '月度支出',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return formatCurrency(value);
                                }
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return formatCurrency(context.raw);
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('載入月度統計資料時發生錯誤:', error);
    }
}

// 載入趨勢圖資料
async function loadTrendData(days) {
    try {
        const data = await apiRequest(`/api/stats/trend?days=${days}`);
        
        if (data.length === 0) {
            document.getElementById('no-trend-data').classList.remove('d-none');
            if (trendChart) {
                trendChart.destroy();
                trendChart = null;
            }
            return;
        }
        
        document.getElementById('no-trend-data').classList.add('d-none');
        
        // 準備圖表資料
        const labels = data.map(item => item.date);
        const values = data.map(item => item.total);
        
        // 創建或更新圖表
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        if (trendChart) {
            trendChart.data.labels = labels;
            trendChart.data.datasets[0].data = values;
            trendChart.update();
        } else {
            trendChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '每日支出',
                        data: values,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        tension: 0.1,
                        pointRadius: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return formatCurrency(value);
                                }
                            }
                        },
                        x: {
                            ticks: {
                                maxRotation: 45,
                                minRotation: 45
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return formatCurrency(context.raw);
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('載入趨勢圖資料時發生錯誤:', error);
    }
}

// 載入統計摘要資料
async function loadSummaryData(startDate, endDate) {
    try {
        let url = '/api/expenses';
        
        if (startDate && endDate) {
            url += `?start_date=${startDate}&end_date=${endDate}`;
        }
        
        const expenses = await apiRequest(url);
        
        if (expenses.length === 0) {
            document.getElementById('total-expense').textContent = '$ 0';
            document.getElementById('avg-daily-expense').textContent = '$ 0';
            document.getElementById('max-expense').textContent = '$ 0';
            document.getElementById('category-count').textContent = '0';
            return;
        }
        
        // 計算總支出
        const totalExpense = expenses.reduce((sum, expense) => sum + parseFloat(expense.amount), 0);
        
        // 計算日期範圍
        const start = new Date(startDate);
        const end = new Date(endDate);
        const daysDiff = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
        
        // 計算平均每日支出
        const avgDailyExpense = totalExpense / daysDiff;
        
        // 找出最高支出
        const maxExpense = Math.max(...expenses.map(expense => parseFloat(expense.amount)));
        
        // 計算不同類別數量
        const uniqueCategories = new Set(expenses.map(expense => expense.category));
        
        // 更新 UI
        document.getElementById('total-expense').textContent = formatCurrency(totalExpense);
        document.getElementById('avg-daily-expense').textContent = formatCurrency(avgDailyExpense);
        document.getElementById('max-expense').textContent = formatCurrency(maxExpense);
        document.getElementById('category-count').textContent = uniqueCategories.size.toString();
    } catch (error) {
        console.error('載入統計摘要時發生錯誤:', error);
    }
}

// 處理統計篩選
function handleFilterStats() {
    const startDate = document.getElementById('stats-start-date').value;
    const endDate = document.getElementById('stats-end-date').value;
    
    if (!startDate || !endDate) {
        showAlert('請選擇開始和結束日期', 'warning');
        return;
    }
    
    loadStatistics();
}

// 下載所有圖表
function downloadAllCharts() {
    try {
        if (categoryChart) {
            downloadChart(categoryChart, '類別支出統計.png');
        }
        
        if (monthlyChart) {
            downloadChart(monthlyChart, '月度支出統計.png');
        }
        
        if (trendChart) {
            downloadChart(trendChart, '支出趨勢圖.png');
        }
        
        showAlert('圖表已下載！');
    } catch (error) {
        console.error('下載圖表時發生錯誤:', error);
        showAlert('下載圖表時發生錯誤', 'danger');
    }
}