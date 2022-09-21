// Chart IDs
let gChartConsumption = null
let gChartUsage = null
let gChartDashboard = null
let gChartHistoryDetailsProduced = null
let gChartHistoryDetailsConsumed = null
let gChartHistoryHighRes = null

// Colors
const FILL_OPACITY = "20";

const COLOR_PRODUCTION_FED_IN = "#2980b9";
const COLOR_PRODUCTION_FED_IN_FILL = COLOR_PRODUCTION_FED_IN + FILL_OPACITY;

const COLOR_PRODUCTION_SELF_CONSUMED = "#27ae60";
const COLOR_PRODUCTION_SELF_CONSUMED_FILL = COLOR_PRODUCTION_SELF_CONSUMED + FILL_OPACITY;

const COLOR_CONSUMED_FROM_GRID = "#8e44ad";
const COLOR_CONSUMED_FROM_GRID_FILL = COLOR_CONSUMED_FROM_GRID + FILL_OPACITY;

const COLOR_CONSUMED_FROM_PV = "#e67e22";

const COLOR_PRODUCED = "#f1c40f";
const COLOR_CONSUMED = "#d35400";


// Utility function to beautify the given date
function utilBeautifyDate(date) {
    if (date.length == 10) {
        // Must be a day
        let day = date.slice(8);
        return parseInt(day).toString();
    }
    else if (date.length == 7) {
        // Must be a month
        let month = date.slice(5);
        return getMonthName(parseInt(month) - 1);
    }
    else {
        // Must be a year
        return date;
    }
}

// Creates a chart showing the consumption distribution
function createConsumptionChart(canvasId, gridPercentage, pvPercentage) {
    var xValues = [getChartString("chart_from_grid"), getChartString("chart_from_pv")];
    var yValues = [gridPercentage, pvPercentage];
    var barColors = [
        COLOR_CONSUMED_FROM_GRID,
        COLOR_CONSUMED_FROM_PV
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
    var xValues = [getChartString("chart_fed_in"), getChartString("chart_self_consumed")];
    var yValues = [fedInPercentage, selfPercentage];
    var barColors = [
        COLOR_PRODUCTION_FED_IN,
        COLOR_PRODUCTION_SELF_CONSUMED
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

    if (gChartDashboard == null) {
        // Create new chart
        const labels = [];
        const chart_data = {
            labels: labels,
            datasets: [{
                label: getChartString("chart_produced_w"),
                data: [],
                fill: true,
                borderColor: COLOR_PRODUCTION_SELF_CONSUMED,
                backgroundColor: COLOR_PRODUCTION_SELF_CONSUMED_FILL,
                borderWidth: 2
            },
            {
                label: getChartString("chart_consumed_w"),
                data: [],
                fill: true,
                borderColor: COLOR_CONSUMED_FROM_GRID,
                backgroundColor: COLOR_CONSUMED_FROM_GRID_FILL,
                borderWidth: 2
            },
            {
                label: getChartString("chart_fed_in_w"),
                data: [],
                fill: true,
                borderColor: COLOR_PRODUCTION_FED_IN,
                backgroundColor: COLOR_PRODUCTION_FED_IN_FILL,
                borderWidth: 2
            }]
        };

        let max = 0.0;
        for (index = data.length - 1; index >= 0; index--) { // Reverse data
            labels.push(data[index][1]); // Element 1 = time
            for (i = 0; i < 3; ++i) {
                let value = data[index][2 + i] * 1000.0;
                chart_data.datasets[i].data.push(value);
                if (value > max) max = value;
            }
        }
        max = (Math.ceil(max) + 100) - (Math.ceil(max) % 100);

        gChartDashboard = new Chart(canvasId, {
            type: "line",
            responsive: true,
            data: chart_data,
            options: {
                maintainAspectRatio: false,
                title: {
                    display: false
                },
                elements: {
                    point: {
                        radius: 0
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        min: 0.0,
                        max: max,
                    }
                },
                locale: getLocale(),
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x',
                        },
                        pan: {
                            enabled: true,
                            mode: 'x',
                        }
                    }
                }
            }
        });
    }
    else {
        // Update chart
        gChartDashboard.data.labels = [];
        gChartDashboard.data.datasets[0].data = [];
        gChartDashboard.data.datasets[1].data = [];
        gChartDashboard.data.datasets[2].data = [];

        let max = 0.0;
        for (index = data.length - 1; index >= 0; index--) { // Reverse data
            gChartDashboard.data.labels.push(data[index][1]); // Element 1 = time
            for (i = 0; i < 3; ++i) {
                let value = data[index][2 + i] * 1000.0;
                gChartDashboard.data.datasets[i].data.push(value);
                if (value > max) max = value;
            }
        }
        max = (Math.ceil(max) + 100) - (Math.ceil(max) % 100);
        gChartDashboard.options.scales.y.max = max;
        gChartDashboard.update();
    }
}

// Creates a chart for the history daily/high res view
function createHighResChart(canvasId, data) {

    if (gChartHistoryHighRes == null) {
        // Create new chart
        const labels = [];
        const chart_data = {
            labels: labels,
            datasets: [{
                label: getChartString("chart_produced_w"),
                data: [],
                fill: true,
                borderColor: COLOR_PRODUCTION_SELF_CONSUMED,
                backgroundColor: COLOR_PRODUCTION_SELF_CONSUMED_FILL,
                borderWidth: 2
            },
            {
                label: getChartString("chart_consumed_w"),
                data: [],
                fill: true,
                borderColor: COLOR_CONSUMED_FROM_GRID,
                backgroundColor: COLOR_CONSUMED_FROM_GRID_FILL,
                borderWidth: 2
            },
            {
                label: getChartString("chart_fed_in_w"),
                data: [],
                fill: true,
                borderColor: COLOR_PRODUCTION_FED_IN,
                backgroundColor: COLOR_PRODUCTION_FED_IN_FILL,
                borderWidth: 2
            }]
        };

        let max = 0.0;
        for (index = 0; index < data.length; index++) {
            labels.push(data[index][0]);
            for (i = 0; i < 3; ++i) {
                let value = data[index][1 + i] * 1000.0;
                chart_data.datasets[i].data.push(value);
                if (value > max) max = value;
            }
        }
        max = (Math.ceil(max) + 100) - (Math.ceil(max) % 100);

        gChartHistoryHighRes = new Chart(canvasId, {
            type: "line",
            responsive: true,
            data: chart_data,
            options: {
                maintainAspectRatio: false,
                title: {
                    display: false
                },
                elements: {
                    point: {
                        radius: 0
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        min: 0.0,
                        max: max,
                    }
                },
                locale: getLocale(),
                plugins: {
                    zoom: {
                        zoom: {
                            wheel: {
                                enabled: true
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: 'x',
                        },
                        pan: {
                            enabled: true,
                            mode: 'x',
                        }
                    }
                }
            }
        });
    }
    else {
        // Update chart
        gChartHistoryHighRes.data.labels = [];
        gChartHistoryHighRes.data.datasets[0].data = [];
        gChartHistoryHighRes.data.datasets[1].data = [];
        gChartHistoryHighRes.data.datasets[2].data = [];

        let max = 0.0;
        for (index = 0; index < data.length; index++) {
            gChartHistoryHighRes.data.labels.push(data[index][0]);
            for (i = 0; i < 3; ++i) {
                let value = data[index][1 + i] * 1000.0;
                gChartHistoryHighRes.data.datasets[i].data.push(value);
                if (value > max) max = value;
            }
        }

        max = (Math.ceil(max) + 100) - (Math.ceil(max) % 100);
        gChartDashboard.options.scales.y.max = max;
        gChartHistoryHighRes.update();
    }
}

// Creates a chart showing history details
function createHistoryDetailsChartProduction(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_produced_self_kwh"),
            data: [],
            borderColor: COLOR_PRODUCTION_SELF_CONSUMED,
            backgroundColor: COLOR_PRODUCTION_SELF_CONSUMED,
            borderWidth: 0,
            stack: 'Stack 0'
        },
        {
            label: getChartString("chart_produced_grid_kwh"),
            data: [],
            borderColor: COLOR_PRODUCTION_FED_IN,
            backgroundColor: COLOR_PRODUCTION_FED_IN,
            borderWidth: 0,
            stack: 'Stack 0'
        }]
    };

    for (index = 0; index < data.length; index++) {
        labels.push(utilBeautifyDate(data[index]["date"])); // Element 1 = time
        chart_data.datasets[0].data.push(data[index]["produced_self"]);
        chart_data.datasets[1].data.push(data[index]["produced_feed_in"]);
    }

    if (gChartHistoryDetailsProduced != null) gChartHistoryDetailsProduced.destroy();
    gChartHistoryDetailsProduced = new Chart(canvasId, {
        type: "bar",
        responsive: true,
        data: chart_data,
        options: {
            maintainAspectRatio: false,
            title: {
                display: false
            },
            plugins: {
                labels: false
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    });
}

// Creates a chart showing history details
function createHistoryDetailsChartConsumption(canvasId, data) {

    const labels = [];
    const chart_data = {
        labels: labels,
        datasets: [{
            label: getChartString("chart_consumed_pv_kwh"),
            data: [],
            borderColor: COLOR_CONSUMED_FROM_PV,
            backgroundColor: COLOR_CONSUMED_FROM_PV,
            borderWidth: 0,
            stack: 'Stack 0'
        },
        {
            label: getChartString("chart_consumed_grid_kwh"),
            data: [],
            borderColor: COLOR_CONSUMED_FROM_GRID,
            backgroundColor: COLOR_CONSUMED_FROM_GRID,
            borderWidth: 0,
            stack: 'Stack 0'
        }]
    };

    for (index = 0; index < data.length; index++) {
        labels.push(utilBeautifyDate(data[index]["date"])); // Element 1 = time
        chart_data.datasets[0].data.push(data[index]["consumed_from_pv"]);
        chart_data.datasets[1].data.push(data[index]["consumed_from_grid"]);
    }

    if (gChartHistoryDetailsConsumed != null) gChartHistoryDetailsConsumed.destroy();
    gChartHistoryDetailsConsumed = new Chart(canvasId, {
        type: "bar",
        responsive: true,
        data: chart_data,
        options: {
            maintainAspectRatio: false,
            title: {
                display: false
            },
            plugins: {
                labels: false
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true
                }
            }
        }
    });
}