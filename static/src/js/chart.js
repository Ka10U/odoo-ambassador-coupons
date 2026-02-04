// Ambassador Coupon Charts
$(document).ready(function() {
    function initCharts() {
        var chartContainers = document.querySelectorAll('[data-code]');
        chartContainers.forEach(function(container) {
            container.style.display = 'flex';
            container.style.justifyContent = 'center';
            container.style.alignItems = 'center';
            container.style.height = '100%';
        });

        $.getJSON('/my/ambassador/coupons/json', function(data) {
            if (data.error) {
                console.error('Error loading chart data:', data.error);
                return;
            }

            chartContainers.forEach(function(container) {
                container.style.display = 'none';
            });

            Object.keys(data).forEach(function(codeId) {
                var codeData = data[codeId];
                var ctx = document.getElementById('chart_' + codeId);
                if (ctx) {
                    var stats = codeData.stats || [];
                    if (stats.length === 0) {
                        ctx.parentElement.innerHTML = '<p class="text-muted text-center py-5">No data available for this period</p>';
                        return;
                    }

                    stats.reverse();
                    var labels = stats.map(function(s) { return s.month; });
                    var totalUsage = stats.map(function(s) { return s.total_usage; });
                    var validatedOrders = stats.map(function(s) { return s.validated_orders; });

                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    label: 'Total Usage',
                                    data: totalUsage,
                                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                                    borderColor: 'rgba(54, 162, 235, 1)',
                                    borderWidth: 1,
                                },
                                {
                                    label: 'Validated Orders',
                                    data: validatedOrders,
                                    backgroundColor: 'rgba(75, 192, 192, 0.7)',
                                    borderColor: 'rgba(75, 192, 192, 1)',
                                    borderWidth: 1,
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'top',
                                    labels: {
                                        usePointStyle: true,
                                        padding: 20
                                    }
                                },
                                tooltip: {
                                    mode: 'index',
                                    intersect: false,
                                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                    titleFont: { size: 14 },
                                    bodyFont: { size: 13 },
                                    padding: 12,
                                    cornerRadius: 4,
                                    callbacks: {
                                        label: function(context) {
                                            var label = context.dataset.label || '';
                                            if (label) {
                                                label += ': ';
                                            }
                                            label += context.parsed.y;
                                            return label;
                                        }
                                    }
                                }
                            },
                            scales: {
                                x: {
                                    stacked: false,
                                    grid: {
                                        display: false
                                    },
                                    ticks: {
                                        maxRotation: 45,
                                        minRotation: 45
                                    }
                                },
                                y: {
                                    stacked: false,
                                    beginAtZero: true,
                                    grid: {
                                        color: 'rgba(0, 0, 0, 0.1)'
                                    },
                                    ticks: {
                                        stepSize: 1
                                    }
                                }
                            },
                            interaction: {
                                mode: 'nearest',
                                axis: 'x',
                                intersect: false
                            }
                        }
                    });
                }
            });
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.error('Failed to load chart data:', textStatus, errorThrown);
            chartContainers.forEach(function(container) {
                container.innerHTML = '<p class="text-danger text-center py-5">Failed to load data</p>';
            });
        });
    }

    if (typeof Chart === 'undefined') {
        console.error('Chart.js not loaded');
        return;
    }

    initCharts();
});
