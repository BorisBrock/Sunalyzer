// Chart IDs
let gChartConsumption = null
let gChartUsage = null
let gChartDashboard = null
let gChartHistoryDetails = null


function createConsumptionChart(canvasId, gridPercentage, pvPercentage) {
    var xValues = ["From grid", "From PV"];
    var yValues = [gridPercentage, pvPercentage];
    var barColors = [
        "#e67e22",
        "#2ecc71"
    ];
    if (gChartConsumption != null) gChartConsumption.destroy();
    gChartConsumption = new Chart(canvasId, {
        type: "doughnut",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: barColors,
                data: yValues
            }]
        },
        options: {
            rotation: 180,
            maintainAspectRatio: false,
            title: {
                display: false
            },
            plugins: {
                labels: {
                    // render 'label', 'value', 'percentage', 'image' or custom function, default is 'percentage'
                    render: 'percentage',
                    fontSize: 16,
                    fontColor: '#ffffff',
                    textShadow: true
                }
            }
        }
    });
}

function createUsageChart(canvasId, fedInPercentage, selfPercentage) {
    var xValues = ["Fed in", "Self consumed"];
    var yValues = [fedInPercentage, selfPercentage];
    var barColors = [
        "#3498db",
        "#9b59b6"
    ];
    if (gChartUsage != null) gChartUsage.destroy();
    gChartUsage = new Chart(canvasId, {
        type: "doughnut",
        data: {
            labels: xValues,
            datasets: [{
                backgroundColor: barColors,
                data: yValues
            }]
        },
        options: {
            rotation: 180,
            maintainAspectRatio: false,
            title: {
                display: false
            },
            plugins: {
                labels: {
                    // render 'label', 'value', 'percentage', 'image' or custom function, default is 'percentage'
                    render: 'percentage',
                    fontSize: 16,
                    fontColor: '#ffffff',
                    textShadow: true
                }
            }
        }
    });
}

function createDashboardChart(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_produced"),
            data: [],
            fill: false,
            borderColor: '#f39c12',
            backgroundColor: '#f39c12',
            borderWidth: 2
        },
        {
            label: getChartString("chart_consumed"),
            data: [],
            fill: false,
            borderColor: '#e74c3c',
            backgroundColor: '#e74c3c',
            borderWidth: 2
        },
        {
            label: getChartString("chart_fed_in"),
            data: [],
            fill: false,
            borderColor: '#3498db',
            backgroundColor: '#3498db',
            borderWidth: 2
        }]
    };

    for (index = 0; index < data.length; index++) {
        labels.push(data[index][1]); // Element 1 = time
        chart_data.datasets[0].data.push(data[index][2]);
        chart_data.datasets[1].data.push(data[index][3]);
        chart_data.datasets[2].data.push(data[index][4]);
    }

    if (gChartDashboard != null) gChartDashboard.destroy();
    gChartDashboard = new Chart(canvasId, {
        type: "line",
        responsive: true,
        data: chart_data,
        options: {
            title: {
                display: false
            },
            elements: {
                point: {
                    radius: 0
                }
            }
        }
    });
}

function createHistoryDetailsChart(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_produced"),
            data: [],
            borderColor: '#f39c12',
            backgroundColor: '#f39c12',
            borderWidth: 2
        },
        {
            label: getChartString("chart_consumed"),
            data: [],
            borderColor: '#e74c3c',
            backgroundColor: '#e74c3c',
            borderWidth: 2
        },
        {
            label: getChartString("chart_fed_in"),
            data: [],
            borderColor: '#3498db',
            backgroundColor: '#3498db',
            borderWidth: 2
        }]
    };

    for (index = 0; index < data.length; index++) {
        labels.push(data[index]["date"]); // Element 1 = time
        chart_data.datasets[0].data.push(data[index]["produced"]);
        chart_data.datasets[1].data.push(data[index]["consumed"]);
        chart_data.datasets[2].data.push(data[index]["fed_in"]);
    }

    if (gChartHistoryDetails != null) gChartHistoryDetails.destroy();
    gChartHistoryDetails = new Chart(canvasId, {
        type: "bar",
        responsive: true,
        data: chart_data,
        options: {
            title: {
                display: false
            },
            plugins: {
                labels: false
              }
        }
    });
}