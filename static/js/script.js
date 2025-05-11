// Modal Functions
function openModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Chart.js Setup
document.addEventListener('DOMContentLoaded', () => {
    // Expense Chart (Main Page)
    const expenseChart = new Chart(document.getElementById('expenseChart'), {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Expenses',
                data: [1200, 1900, 300, 500, 2000, 3000],
                backgroundColor: '#EF4444', // Red-500
                borderColor: '#B91C1C', // Red-700
                borderWidth: 1
            }]
        },
        options: {
            animation: { duration: 1000, easing: 'easeOutQuart' },
            scales: { y: { beginAtZero: true } }
        }
    });

    // Pie Chart (Main Page)
    const pieChart = new Chart(document.getElementById('pieChart'), {
        type: 'pie',
        data: {
            labels: ['Income', 'Expenses'],
            datasets: [{
                data: [3500, 2270],
                backgroundColor: ['#10B981', '#EF4444'], // Green-500, Red-500
                borderColor: ['#047857', '#B91C1C'], // Green-700, Red-700
                borderWidth: 1
            }]
        },
        options: {
            animation: { duration: 1000, easing: 'easeOutQuart' }
        }
    });

    // Bar Chart (Reports Page)
    const barChart = new Chart(document.getElementById('barChart'), {
        type: 'bar',
        data: {
            labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
            datasets: [
                {
                    label: 'Income',
                    data: [500, 700, 300, 800, 600, 900, 400],
                    backgroundColor: '#10B981', // Green-500
                    borderColor: '#047857', // Green-700
                    borderWidth: 1
                },
                {
                    label: 'Expenses',
                    data: [300, 400, 200, 500, 350, 600, 250],
                    backgroundColor: '#EF4444', // Red-500
                    borderColor: '#B91C1C', // Red-700
                    borderWidth: 1
                }
            ]
        },
        options: {
            animation: { duration: 1000, easing: 'easeOutQuart' },
            scales: { y: { beginAtZero: true } }
        }
    });

    // Expense Pie Chart (Reports Page)
    const expensePieChart = new Chart(document.getElementById('expensePieChart'), {
        type: 'pie',
        data: {
            labels: ['Rent', 'Groceries', 'Utilities', 'Entertainment'],
            datasets: [{
                data: [1200, 500, 300, 270],
                backgroundColor: ['#3B82F6', '#FBBF24', '#10B981', '#EF4444'], // Blue-500, Yellow-400, Green-500, Red-500
                borderColor: ['#1D4ED8', '#D97706', '#047857', '#B91C1C'], // Blue-700, Yellow-600, Green-700, Red-700
                borderWidth: 1
            }]
        },
        options: {
            animation: { duration: 1000, easing: 'easeOutQuart' }
        }
    });
});

// Date Range Filter for Reports
function filterReports(range) {
    // Placeholder for updating chart data based on range
    console.log(`Filtering reports for: ${range}`);
    // Example: Update barChart data
    // barChart.data.datasets[0].data = newData; // Update with backend data
    // barChart.update();
}