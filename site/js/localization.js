
let gLangEn = 1;
let gLangDe = 2;

let gCurLang = gLangEn;

let translations = [
    // HTML element ID              English (1)     German (2)

    // Navigation bar
    ["navbar_dropdown_language",        "Language",         "Sprache"],

    // Side bar
    ["sidebar_headline_overview",       "Overview",         "Übersicht"],
    ["sidebar_today",                   "Today",            "Heute"],
    ["sidebar_headline_history",        "History",          "Historie"],
    ["sidebar_by_day",                  "By Day",           "Nach Tag"],
    ["sidebar_by_month",                "By Month",         "Nach Monat"],
    ["sidebar_by_year",                 "By Year",          "Nach Jahr"],
    ["sidebar_all_time",                "All Time",         "Gesamt"],

    // Dashboard
    ["dashboard_subtitle",              "Last updated: ",   "Letzte Aktualisierung: "],

    ["dash_card_current",               "Current",          "Momentanwerte"],
    ["dash_card_today",                 "Today",            "Heutige Werte"],
    ["dash_card_all_time",              "All Time",         "Allzeit-Werte"],
    ["dash_card_24h",                   "Last 24 Hours",    "Die letzten 24 Stunden"],

    ["dash_text_currently_produced",    "Produced",         "Erzeugt"],
    ["dash_text_currently_consumed",    "Consumed",         "Vebraucht"],
    ["dash_text_currently_fed_in",      "Fed in",           "Eingespeist"],

    ["dash_text_today_produced",        "Produced",          "Erzeugt"],
    ["dash_text_today_consumed",        "Consumed",          "Vebraucht"],
    ["dash_text_today_fed_in",          "Fed in",            "Eingespeist"],
    ["dash_text_today_earned",          "Earned",            "Verdient"],

    ["dash_text_all_time_produced",     "Produced",          "Erzeugt"],
    ["dash_text_all_time_consumed",     "Consumed",          "Vebraucht"],
    ["dash_text_all_time_fed_in",       "Fed in",            "Eingespeist"],
    ["dash_text_all_time_earned",       "Earned",            "Verdient"],

    // History
    ["history_card_production",         "PV Production",                "Erzeugt"],
    ["history_card_earned",             "Earnings",                     "Verdienst"],
    ["history_card_usage",              "Usage of Produced Energy",     "Verwendung der erzeugten Energie"],
    ["history_card_consumption",        "Power Consumption",            "Energieverbrauch"],
    ["history_text_produced",           "Energy produced",              "Erzeugte PV-Energie"],
    ["history_text_earned_feedin",      "Earned with feed-in",          "Verdienst durch Einspeisung"],
    ["history_text_earned_self",        "Saved via self-consumption",   "Ersparnis durch Eigenverbrauch"],
    ["history_text_earned_total",       "Total",                        "Summe"],
    ["history_text_fedin",              "Fed into the grid",            "Ins Netz eingespeist"],
    ["history_text_self_consumed",      "Self consumed",                "Selbst verbraucht"],
    ["history_text_consumption_grid",   "Consumption from grid",        "Verbrauch aus dem Netz"],
    ["history_text_consumption_self",   "Consumption from PV",          "Verbrauch aus PV"],
    ["history_text_consumption_total",  "Total consumption",            "Gesamtverbrauch"],
    ["history_card_graph_text",          "Details",                      "Zeitverlauf"],

    // Months combo box
    ["cbx_month_1",     "January",      "Januar"],
    ["cbx_month_2",     "February",     "Februar"],
    ["cbx_month_3",     "March",        "März"],
    ["cbx_month_4",     "April",        "April"],
    ["cbx_month_5",     "May",          "Mai"],
    ["cbx_month_6",     "June",         "Juni"],
    ["cbx_month_7",     "July",         "Juli"],
    ["cbx_month_8",     "August",       "August"],
    ["cbx_month_9",     "September",    "September"],
    ["cbx_month_10",    "October",      "Oktober"],
    ["cbx_month_11",    "November",     "November"],
    ["cbx_month_12",    "December",     "Dezember"],

    // Info
    ["info_no_data",    "No data is available for the selected time span.",     "Für den gewählten Zeitraum liegen keine Daten vor."],
];

let chartStrings = [
    // HTML element ID      English (1)             German (2)
    ["chart_produced",      "Produced [kWh]",       "Erzeugt [kWh]"],
    ["chart_consumed",      "Consumed [kWh]",       "Verbraucht [kWh]"],
    ["chart_fed_in",        "Fed in [kWh]",         "Eingespeist [kWh]"],
];

let historyStrings = [
    // HTML element ID      English (1)             German (2)
    ["daily_data",          "Daily Data",           "Daten nach Tag"],
    ["monthly_data",        "Monthly Data",         "Daten nach Monat"],
    ["yearly_data",         "Yearly Data",          "Daten nach Jahr"],
    ["all_time_data",       "All Time Data",        "Allzeitdaten"],
];


function restoreLanguage() {
    var lang = localStorage.getItem("lang");
    if(lang != null)
        switchLanguageByIndex(parseInt(lang));
}

function switchLanguageToEnglish() {
    switchLanguageByIndex(gLangEn);
}

function switchLanguageToGerman() {
    switchLanguageByIndex(gLangDe);
}

function switchLanguageByIndex(index) {
    gCurLang = index;
    localStorage.setItem("lang", index)
    translations.forEach(translation => {
        document.getElementById(translation[0]).innerHTML = translation[index];
    });
}

function getChartString(id) {
    for(i=0; i<chartStrings.length; ++i)
        if(chartStrings[i][0] == id)
            return chartStrings[i][gCurLang];
    return "...";
}

function getHistoryString(id) {
    for(i=0; i<historyStrings.length; ++i)
        if(historyStrings[i][0] == id)
            return historyStrings[i][gCurLang];
    return "...";
}