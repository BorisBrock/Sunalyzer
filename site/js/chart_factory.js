// Chart IDs
let gChartConsumption = null
let gChartUsage = null
let gChartDashboard = null
let gChartHistoryDetails = null

// Colors
const COLOR_CONSUMED_GRID   = "#d35400";
const COLOR_CONSUMED_PV     = "#f1c40f";
const COLOR_SELF_CONSUMED   = "#f1c40f";
const COLOR_FED_IN          = "#3498db";
const COLOR_PRODUCED        = "#f1c40f";
const COLOR_CONSUMED        = "#d35400";


// Creates a chart showing the consumption distribution
function createConsumptionChart(canvasId, gridPercentage, pvPercentage) {
    var xValues = ["From grid", "From PV"];
    var yValues = [gridPercentage, pvPercentage];
    var barColors = [
        COLOR_CONSUMED_GRID,
        COLOR_CONSUMED_PV
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

// Creates a chart showing the power consumption distribution
function createUsageChart(canvasId, fedInPercentage, selfPercentage) {
    var xValues = ["Fed in", "Self consumed"];
    var yValues = [fedInPercentage, selfPercentage];
    var barColors = [
        COLOR_FED_IN,
        COLOR_SELF_CONSUMED
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

// Creates a chart for the dashboard view
function createDashboardChart(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_produced"),
            data: [],
            fill: false,
            borderColor: COLOR_PRODUCED,
            backgroundColor: COLOR_PRODUCED,
            borderWidth: 2
        },
        {
            label: getChartString("chart_consumed"),
            data: [],
            fill: false,
            borderColor: COLOR_CONSUMED,
            backgroundColor: COLOR_CONSUMED,
            borderWidth: 2
        },
        {
            label: getChartString("chart_fed_in"),
            data: [],
            fill: false,
            borderColor: COLOR_FED_IN,
            backgroundColor: COLOR_FED_IN,
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

// Creates a chart showing history details
function createHistoryDetailsChart(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_produced"),
            data: [],
            borderColor: COLOR_PRODUCED,
            backgroundColor: COLOR_PRODUCED,
            borderWidth: 2
        },
        {
            label: getChartString("chart_consumed"),
            data: [],
            borderColor: COLOR_CONSUMED,
            backgroundColor: COLOR_CONSUMED,
            borderWidth: 2
        },
        {
            label: getChartString("chart_fed_in"),
            data: [],
            borderColor: COLOR_FED_IN,
            backgroundColor: COLOR_FED_IN,
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