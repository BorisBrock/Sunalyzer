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

let gCurDate = new Date();
let gMinDate = null

let gDahboardGraphTimespan = 24


// Called when index.html has finished loading
window.addEventListener('DOMContentLoaded', event => {
    gBaseUrl = document.baseURI;
    console.log("Setting base URI to " + gBaseUrl);
    restoreLanguage();
    setInterval(updateTime, 1000);
    setInterval(updateCurrentStats, 3000);
    setInterval(updateRealTimeGraph, 5000);
    restoreSettings();
    showViewDashboard();
    updateCurrentStats();
    updateRealTimeGraph();
    initSelectionBoxes();
    updateCsvDateSelector();
    setVersion();
    setName();
});

function setName() {
    fetchNameJSON().then(name =>{
        document.getElementById("instance-name").innerHTML = "Sunalyzer "+name;
        document.title ="Sunalyzer "+ name;
    })    
  }

  async function fetchNameJSON() {
    const response = await fetch(gBaseUrl + 'name');
    const name = await response.json();
    return name;
}

function restoreSettings() {
    var ts = localStorage.getItem("dash_time_span");
    if (ts != null)
        gDahboardGraphTimespan = parseInt(ts);
}

// Called cyclically to update the current stats
function updateCurrentStats() {
    if (!gDashboardVisible) return;
    //console.log("Refreshing dashbard");
    fetchCurrentStatsJSON().then(stats => {
        //console.log(stats);
        const d = new Date();
        document.getElementById("dashboard_subtitle_time").innerHTML = d.toLocaleTimeString('de-DE');

        document.getElementById("dash_today_produced").innerHTML = numFormat(stats["today_produced_kwh"] * 1000.0, 0);
        document.getElementById("dash_today_consumed").innerHTML = numFormat(stats["today_consumed_kwh"] * 1000.0, 0);
        document.getElementById("dash_today_fed_in").innerHTML = numFormat(stats["today_fed_in_kwh"] * 1000.0, 0);
        document.getElementById("dash_today_earned").innerHTML = numFormat(stats["today_earned"], 2);
        document.getElementById("dash_today_autarky").innerHTML = numFormat(stats["today_autarky"], 0);

        document.getElementById("dash_all_time_produced").innerHTML = numFormat(stats["all_time_produced_kwh"], 0);
        document.getElementById("dash_all_time_consumed").innerHTML = numFormat(stats["all_time_consumed_kwh"], 0);
        document.getElementById("dash_all_time_fed_in").innerHTML = numFormat(stats["all_time_fed_in_kwh"], 0);
        document.getElementById("dash_all_time_earned").innerHTML = numFormat(stats["all_time_earned"], 2);
        document.getElementById("dash_all_time_autarky").innerHTML = numFormat(stats["all_time_autarky"], 0);

        // Info graphic
        updateInfoGraphic(
            Math.floor(stats["currently_produced_w"]), 
            Math.floor(stats["currently_consumed_grid_w"]),
            Math.floor(stats["currently_fed_in_w"]));
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
    //console.log("Refreshing dashbard");
    fetchRealTimeStatsJSON().then(stats => {
        createDashboardChart("chart_dashboard", stats);
    });
}

// Async function to get the real time stats
async function fetchRealTimeStatsJSON() {
    const response = await fetch(gBaseUrl + 'query?type=real_time&h=' + gDahboardGraphTimespan);
    const stats = await response.json();
    return stats;
}

function initSelectionBoxes() {
    // Days: numbers 1 to 31
    for (let i = 1; i <= 31; i++) {
        addSelectionItem("selection_day2", i.toString(), i.toString());
        addSelectionItem("csv_selection_day2", i.toString(), i.toString());
    }
    // Years: query from DB
    fetchDatesJSON().then(dates => {
        //console.log(stats);
        gMinDate = new Date(dates["year_min"] + "-01-01");
        for (let i = dates["year_min"]; i <= dates["year_max"]; i++) {
            addSelectionItem("selection_year2", i.toString(), i.toString());
            addSelectionItem("csv_selection_year2", i.toString(), i.toString());
        }
        // Initial selection
        selectDate(new Date());
    });
}

function selectDate(date) {
    gCurDate = date;
    // Combo boxes 1
    document.getElementById('selection_year2').value = date.getFullYear();
    document.getElementById('selection_month2').value = date.getMonth() + 1;
    document.getElementById('selection_day2').value = date.getDate();
    // Combo boxes 2
    document.getElementById('csv_selection_year2').value = date.getFullYear();
    document.getElementById('csv_selection_month2').value = date.getMonth() + 1;
    document.getElementById('csv_selection_day2').value = date.getDate();
}

// Async function to get the important dates
async function fetchDatesJSON() {
    const response = await fetch(gBaseUrl + 'query?type=dates');
    const stats = await response.json();
    return stats;
}


// Called cyclically to update the current stats
function updateHistoryStats() {
    // Store data
    let year = document.getElementById('selection_year2').value.toString();
    let month = document.getElementById('selection_month2').value.toString();
    let day = document.getElementById('selection_day2').value.toString();
    gCurDate = new Date(year + "-" + month + "-" + day);
    // Update stats
    fetchHistoryStatsJSON().then(stats => {
        //console.log(stats);
        if (stats["state"] == "ok") {
            setElementVisible("row_error_banner", false);
            setElementVisible("row_history_data", true);
            setElementVisible("history_card_high_res", true);   

            document.getElementById("history_stat_produced").innerHTML = numFormat(stats["produced_kwh"], 2);

            document.getElementById("history_stat_self_consumed").innerHTML = numFormat(stats["consumed_from_pv_kwh"], 2);
            document.getElementById("history_stat_fedin").innerHTML = numFormat(stats["usage_fed_in_kwh"], 2);

            document.getElementById("history_stat_consumption_grid").innerHTML = numFormat(stats["consumed_from_grid_kwh"], 2);
            document.getElementById("history_stat_consumption_self").innerHTML = numFormat(stats["consumed_from_pv_kwh"], 2);
            document.getElementById("history_stat_consumption_total").innerHTML = numFormat(stats["consumed_total_kwh"], 2);

            document.getElementById("history_stat_earned_feedin").innerHTML = numFormat(stats["earned_feedin"], 2);
            document.getElementById("history_stat_earned_self").innerHTML = numFormat(stats["earned_savings"], 2);
            document.getElementById("history_stat_earned_total").innerHTML = numFormat(stats["earned_total"], 2);

            document.getElementById("history_stat_autarky").innerHTML = numFormat(stats["autarky"], 0);

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

            // Create high res chart
            if(stats["high_res"] != "") {
                data = JSON.parse(stats["high_res"])
                createHighResChart("chart_history_high_res", data);
                setElementVisible("history_card_high_res", true);
            } else {
                setElementVisible("history_card_high_res", false);
            }
        }
        else {
            setElementVisible("row_error_banner", true);
            setElementVisible("row_history_data", false);
            setElementVisible("history_card_high_res", false);
        }
    });

    // Also update the details graph
    if (gCurHistory == histories.MONTH || gCurHistory == histories.YEAR || gCurHistory == histories.ALL)
        updateHistoryDetailsGraphs();
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
    //console.log("Refreshing historic stats: " + query);
    const response = await fetch(gBaseUrl + query);
    const stats = await response.json();
    return stats;
}

function updateHistoryDetailsGraphs() {
    fetchHistoryDetailsJSON().then(stats => {
        //console.log(stats);
        createHistoryDetailsChartProduction("chart_history_details_production", stats);
        createHistoryDetailsChartConsumption("chart_history_details_consumption", stats);
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

function updateStatistics() {
    // Update stats
    fetchStatisticsJSON().then(stats => {
        //console.log(stats);
        if (stats["state"] == "ok") {
            document.getElementById("stats_highest_prod_value").innerHTML = numFormat(stats["highest_production_w"], 0) + " W";
            document.getElementById("stats_highest_prod_date").innerHTML = prettyPrintDateString(stats["highest_production_date"]);

            document.getElementById("stats_best_day_value").innerHTML = numFormat(stats["best_day_production_kwh"], 2) + " kWh";
            document.getElementById("stats_best_day_date").innerHTML = prettyPrintDateString(stats["best_day_date"]);

            document.getElementById("stats_best_month_value").innerHTML = numFormat(stats["best_month_production_kwh"], 2) + " kWh";
            document.getElementById("stats_best_month_date").innerHTML = prettyPrintDateStringWithoutDay(stats["best_month_date"]);

            document.getElementById("stats_best_year_value").innerHTML = numFormat(stats["best_year_production_kwh"], 2) + " kWh";
            document.getElementById("stats_best_year_date").innerHTML = "in " + stats["best_year_date"];

            document.getElementById("statistics_value_avg_daily_prod").innerHTML = numFormat(stats["average_daily_production_kwh"], 2);

            document.getElementById("statistics_value_start_date").innerHTML = prettyPrintDateString(stats["start_of_operation"]);
            document.getElementById("statistics_value_runtime").innerHTML = stats["days_of_operation"] + " " + getUnitDays();
        }
    });
}

// Async function to get the statistics stats
async function fetchStatisticsJSON() {
    const response = await fetch(gBaseUrl + 'query?type=statistics');
    const stats = await response.json();
    return stats;
}



function showViewDashboard() {
    setElementVisible("view_dashboard", true);
    setElementVisible("view_statistics", false);
    setElementVisible("view_history", false);
    setElementVisible("view_csv", false);
    setInfoGraphicEnabled(true);
    gDashboardVisible = true;
}

function showViewStatistics() {
    setElementVisible("view_dashboard", false);
    setElementVisible("view_statistics", true);
    setElementVisible("view_history", false);
    setElementVisible("view_csv", false);
    setInfoGraphicEnabled(false);
    gDashboardVisible = false;
    updateStatistics();
}

function showViewHistory(mode) {
    setElementVisible("view_dashboard", false);
    setElementVisible("view_statistics", false);
    setElementVisible("view_history", true);
    setElementVisible("view_csv", false);
    setInfoGraphicEnabled(false);
    gDashboardVisible = false;
    gCurHistory = mode;

    switch (mode) {
        case histories.TODAY:
            selectDate(new Date());
            document.getElementById("headline_history").innerHTML = getHistoryString("daily_data");
            setElementVisible("selection_prev", true);
            setElementVisible("selection_next", true);
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", true);
            setElementVisible("history_card_graphs", false);
            setElementVisible("history_card_high_res", true);
        case histories.DAY:
            document.getElementById("headline_history").innerHTML = getHistoryString("daily_data");
            setElementVisible("selection_prev", true);
            setElementVisible("selection_next", true);
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", true);
            setElementVisible("history_card_graphs", false);
            setElementVisible("history_card_high_res", true);
            break;
        case histories.MONTH:
            document.getElementById("headline_history").innerHTML = getHistoryString("monthly_data");
            setElementVisible("selection_prev", true);
            setElementVisible("selection_next", true);
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", true);
            setElementVisible("selection_day", false);
            setElementVisible("history_card_high_res", false);
            // Show the days
            setElementVisible("history_card_graphs", true);
            break;
        case histories.YEAR:
            document.getElementById("headline_history").innerHTML = getHistoryString("yearly_data");
            setElementVisible("selection_prev", true);
            setElementVisible("selection_next", true);
            setElementVisible("selection_year", true);
            setElementVisible("selection_month", false);
            setElementVisible("selection_day", false);
            setElementVisible("history_card_high_res", false);
            // Show the months
            setElementVisible("history_card_graphs", true);
            break;
        case histories.ALL:
            document.getElementById("headline_history").innerHTML = getHistoryString("all_time_data");
            setElementVisible("selection_prev", false);
            setElementVisible("selection_next", false);
            setElementVisible("selection_year", false);
            setElementVisible("selection_month", false);
            setElementVisible("selection_day", false);
            setElementVisible("history_card_high_res", false);
            // Show the years
            setElementVisible("history_card_graphs", true);
            break;
    }
    updateHistoryStats();
}

function showViewCsv() {
    setElementVisible("view_dashboard", false);
    setElementVisible("view_statistics", false);
    setElementVisible("view_history", false);
    setElementVisible("view_csv", true);
    setInfoGraphicEnabled(false);
    gDashboardVisible = false;
}

function updateCsvDateSelector() {
    if (document.getElementById("csv_range_rad_day").checked == true) {
        setElementVisible("csv_selection_year", true);
        setElementVisible("csv_selection_month", true);
        setElementVisible("csv_selection_day", true);

        setElementEnabled("csv_res_rad_day", true);
        setElementEnabled("csv_res_rad_month", false);
        setElementEnabled("csv_res_rad_year", false);

        if (isElementChecked("csv_res_rad_month") || isElementChecked("csv_res_rad_year"))
            setElementChecked("csv_res_rad_day", true);
    }
    else if (document.getElementById("csv_range_rad_month").checked == true) {
        setElementVisible("csv_selection_year", true);
        setElementVisible("csv_selection_month", true);
        setElementVisible("csv_selection_day", false);

        setElementEnabled("csv_res_rad_day", true);
        setElementEnabled("csv_res_rad_month", false);
        setElementEnabled("csv_res_rad_year", false);

        if (isElementChecked("csv_res_rad_month") || isElementChecked("csv_res_rad_year"))
            setElementChecked("csv_res_rad_day", true);
    }
    else if (document.getElementById("csv_range_rad_year").checked == true) {
        setElementVisible("csv_selection_year", true);
        setElementVisible("csv_selection_month", false);
        setElementVisible("csv_selection_day", false);

        setElementEnabled("csv_res_rad_day", true);
        setElementEnabled("csv_res_rad_month", true);
        setElementEnabled("csv_res_rad_year", false);

        if (isElementChecked("csv_res_rad_year"))
            setElementChecked("csv_res_rad_month", true);
    }
    else {
        setElementVisible("csv_selection_year", false);
        setElementVisible("csv_selection_month", false);
        setElementVisible("csv_selection_day", false);

        setElementEnabled("csv_res_rad_day", true);
        setElementEnabled("csv_res_rad_month", true);
        setElementEnabled("csv_res_rad_year", true);
    }
}


function datePrev() {
    let date = new Date(gCurDate)
    if (gCurHistory == histories.DAY || gCurHistory == histories.TODAY) {
        date.setDate(date.getDate() - 1);
    }
    else if (gCurHistory == histories.MONTH) {
        date.setMonth(date.getMonth() - 1);
    }
    else if (gCurHistory == histories.YEAR) {
        date.setFullYear(date.getFullYear() - 1);
    }

    if (date < gMinDate) date = new Date(gMinDate);

    selectDate(date);
    updateHistoryStats();
}

function dateNext() {
    let date = new Date(gCurDate)
    if (gCurHistory == histories.DAY || gCurHistory == histories.TODAY) {
        date.setDate(date.getDate() + 1);
    }
    else if (gCurHistory == histories.MONTH) {
        date.setMonth(date.getMonth() + 1);
    }
    else if (gCurHistory == histories.YEAR) {
        date.setFullYear(date.getFullYear() + 1);
    }

    const maxDate = new Date()
    if (date > maxDate) date = new Date(maxDate);

    selectDate(date);
    updateHistoryStats();
}

function changeDashboardGraphTimeSpan(hours) {
    gDahboardGraphTimespan = hours;
    localStorage.setItem("dash_time_span", gDahboardGraphTimespan);
    updateRealTimeGraph();
}



function setElementVisible(name, visible) {
    document.getElementById(name).style.display = visible ? 'block' : 'none';
}

function setElementEnabled(name, enabled) {
    if (enabled)
        document.getElementById(name).removeAttribute("disabled");
    else
        document.getElementById(name).setAttribute("disabled", "");
}

function isElementChecked(name) {
    return document.getElementById(name).checked;
}

function setElementChecked(name, checked) {
    document.getElementById(name).checked = checked;
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