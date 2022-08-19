// This base URL is used as the destination for REST query calls
var gBaseUrl = "";

// Global status flag
var gDashboardVisible = false;


// History types
const histories = {
    TODAY: 'today',
    DAY: 'day',
    MONTH: 'month',
    YEAR: 'year',
    ALL: 'all'
}

let gCurHistory = histories.DAY;


// Called when index.html has finished loading
window.addEventListener('DOMContentLoaded', event => {
    gBaseUrl = document.baseURI;
    console.log("Setting base URI to " + gBaseUrl);
    restoreLanguage();
    setInterval(updateTime, 1000);
    setInterval(updateCurrentStats, 3000);
    setInterval(updateRealTimeGraph, 60000);
    showViewDashboard();
    updateCurrentStats();
    updateRealTimeGraph();
    initSelectionBoxes();
    setVersion();
});

// Called cyclically to update the current stats
function updateCurrentStats() {
    if (!gDashboardVisible) return;
    console.log("Refreshing dashbard");
    fetchCurrentStatsJSON().then(stats => {
        console.log(stats);
        const d = new Date();
        document.getElementById("dashboard_subtitle_time").innerHTML = d.toLocaleTimeString('de-DE');

        document.getElementById("dash_currently_produced").innerHTML = numFormat(stats["currently_produced_kw"], 2);
        document.getElementById("dash_currently_consumed").innerHTML = numFormat(stats["currently_consumed_kw"], 2);
        document.getElementById("dash_currently_fed_in").innerHTML = numFormat(stats["currently_fed_in_kw"]), 2;

        document.getElementById("dash_today_produced").innerHTML = numFormat(stats["today_produced_kwh"], 0);
        document.getElementById("dash_today_consumed").innerHTML = numFormat(stats["today_consumed_kwh"], 0);
        document.getElementById("dash_today_fed_in").innerHTML = numFormat(stats["today_fed_in_kwh"], 0);
        document.getElementById("dash_today_earned").innerHTML = numFormat(stats["today_earned"], 0);

        document.getElementById("dash_all_time_produced").innerHTML = numFormat(stats["all_time_produced_kwh"], 0);
        document.getElementById("dash_all_time_consumed").innerHTML = numFormat(stats["all_time_consumed_kwh"], 0);
        document.getElementById("dash_all_time_fed_in").innerHTML = numFormat(stats["all_time_fed_in_kwh"], 0);
        document.getElementById("dash_all_time_earned").innerHTML = numFormat(stats["all_time_earned"], 0);
    });
}

// Called cyclically to update the time
function updateTime() {
    const d = new Date();
    let text = d.toLocaleTimeString('de-DE');
    document.getElementById("time").innerHTML = text;
}

// Async function to get the current stats
async function fetchCurrentStatsJSON() {
    const response = await fetch(gBaseUrl + 'query?type=current');
    const stats = await response.json();
    return stats;
}

// Called cyclically to update the current stats
function updateRealTimeGraph() {
    if (!gDashboardVisible) return;
    console.log("Refreshing dashbard");
    fetchRealTimeStatsJSON().then(stats => {
        createDashboardChart("chart_dashboard", stats);
    });
}

// Async function to get the real time stats
async function fetchRealTimeStatsJSON() {
    const response = await fetch(gBaseUrl + 'query?type=real_time');
    const stats = await response.json();
    return stats;
}

function initSelectionBoxes() {
    // Days: numbers 1 to 31
    for (let i = 1; i <= 31; i++) {
        addSelectionItem("selection_day2", i.toString(), i.toString());
    }
    // Years: query from DB
    fetchDatesJSON().then(dates => {
        //console.log(stats);
        for (let i = dates["year_min"]; i <= dates["year_max"]; i++) {
            addSelectionItem("selection_year2", i.toString(), i.toString());
        }
        // Initial selection
        selectDateToday();
    });
}

function selectDateToday() {
    document.getElementById('selection_year2').value = new Date().getFullYear();
    document.getElementById('selection_month2').value = new Date().getMonth() + 1;
    document.getElementById('selection_day2').value = new Date().getDate();
}

// Async function to get the important dates
async function fetchDatesJSON() {
    const response = await fetch(gBaseUrl + 'query?type=dates');
    const stats = await response.json();
    return stats;
}


// Called cyclically to update the current stats
function updateHistoryStats() {
    fetchHistoryStatsJSON().then(stats => {
        console.log(stats);

        if (stats["state"] == "ok") {
            setElementVisible("row_error_banner", false);
            setElementVisible("row_history_data", true);

            document.getElementById("history_stat_produced").innerHTML = numFormat(stats["produced_kwh"], 2);

            document.getElementById("history_stat_self_consumed").innerHTML = numFormat(stats["consumed_from_pv_kwh"], 2);
            document.getElementById("history_stat_fedin").innerHTML = numFormat(stats["usage_fed_in_kwh"], 2);

            document.getElementById("history_stat_consumption_grid").innerHTML = numFormat(stats["consumed_from_grid_kwh"], 2);
            document.getElementById("history_stat_consumption_self").innerHTML = numFormat(stats["consumed_from_pv_kwh"], 2);
            document.getElementById("history_stat_consumption_total").innerHTML = numFormat(stats["consumed_total_kwh"], 2);

            document.getElementById("history_stat_earned_feedin").innerHTML = numFormat(stats["earned_feedin"], 2);
            document.getElementById("history_stat_earned_self").innerHTML = numFormat(stats["earned_savings"], 2);
            document.getElementById("history_stat_earned_total").innerHTML = numFormat(stats["earned_total"], 2);

            // Create the consumption doughnut chart
            createConsumptionChart(
                "chart_consumption",
                parseFloat(stats["consumed_from_grid_percent"]),
                parseFloat(stats["consumed_from_pv_percent"]));

            // Create the usage doughnut chart
            createUsageChart(
                "chart_usage",
                parseFloat(stats["usage_fed_in_percent"]),
                parseFloat(stats["usage_self_consumed_percent"]));
        }
        else {
            setElementVisible("row_error_banner", true);
            setElementVisible("row_history_data", false);
        }
    });

    // Also update the details graph
    if(gCurHistory == histories.MONTH || gCurHistory == histories.YEAR || gCurHistory == histories.ALL)
    updateHistoryDetailsGraph();
}

// Async function to get the current stats
async function fetchHistoryStatsJSON() {
    // Build query
    let query = "query?type=historical&table=";
    switch (gCurHistory) {
        case histories.TODAY:
        case histories.DAY:
            query += "days&date=";
            query += document.getElementById('selection_year2').value.toString();
            query += "-";
            query += padStr(document.getElementById('selection_month2').value.toString());
            query += "-";
            query += padStr(document.getElementById('selection_day2').value.toString());
            break;
        case histories.MONTH:
            query += "months&date=";
            query += document.getElementById('selection_year2').value.toString();
            query += "-";
            query += padStr(document.getElementById('selection_month2').value.toString());
            break;
        case histories.YEAR:
            query += "years&date=";
            query += document.getElementById('selection_year2').value.toString();
            break;
        case histories.ALL:
            query += "all_time&date=all_time";
            break;
    }
    console.log("Refreshing historic stats: " + query);
    const response = await fetch(gBaseUrl + query);
    const stats = await response.json();
    return stats;
}

function updateHistoryDetailsGraph() {
    fetchHistoryDetailsJSON().then(stats => {
        //console.log(stats);
        createHistoryDetailsChart("chart_history_details", stats);
    });
}

// Async function to get the current stats
async function fetchHistoryDetailsJSON() {
    // Build query
    let query = "query?type=";
    switch (gCurHistory) {
        case histories.MONTH:
            query += "days_in_month&date=";
            query += document.getElementById('selection_year2').value.toString();
            query += "-";
            query += padStr(document.getElementById('selection_month2').value.toString());
            break;
        case histories.YEAR:
            query += "months_in_year&date=";
            query += document.getElementById('selection_year2').value.toString();
            break;
        case histories.ALL:
            query += "years_in_all_time";
            break;
    }
    const response = await fetch(gBaseUrl + query);
    const stats = await response.json();
    return stats;
}



function showViewDashboard() {
    setElementVisible("view_dashboard", true);
    setElementVisible("view_history", false);
    gDashboardVisible = true;
}

function showViewHistory(mode) {
    setElementVisible("view_dashboard", false);
    setElementVisible("view_history", true);
    gDashboardVisible = false;
    gCurHistory = mode;

    switch (mode) {
        case histories.TODAY:
            selectDateToday();
            document.getElementById("headline_history").innerHTML = getHistoryString("daily_data");
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", true);
            setElementVisible("history_card_graph", false);
        case histories.DAY:
            document.getElementById("headline_history").innerHTML = getHistoryString("daily_data");
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", true);
            setElementVisible("history_card_graph", false);
            break;
        case histories.MONTH:
            document.getElementById("headline_history").innerHTML = getHistoryString("monthly_data");
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", false);
            // Show the days
            setElementVisible("history_card_graph", true);
            break;
        case histories.YEAR:
            document.getElementById("headline_history").innerHTML = getHistoryString("yearly_data");
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", false);
            setElementVisible("selection_day", false);
            // Show the months
            setElementVisible("history_card_graph", true);
            break;
        case histories.ALL:
            document.getElementById("headline_history").innerHTML = getHistoryString("all_time_data");
            setElementVisible("selection_year", false);
            setElementVisible("selection_month", false);
            setElementVisible("selection_day", false);
            setElementVisible("history_card_graph", false);
            // Show the years
            setElementVisible("history_card_graph", true);
            break;
    }
    updateHistoryStats();
}

function setElementVisible(name, visible) {
    document.getElementById(name).style.display = visible ? 'block' : 'none';
}

function addSelectionItem(control, name, value) {
    const node = document.createElement("option");
    node.setAttribute("value", value);
    const textnode = document.createTextNode(name);
    node.appendChild(textnode);
    document.getElementById(control).appendChild(node);
}

function padStr(i) {
    return (i < 10) ? "0" + i : "" + i;
}