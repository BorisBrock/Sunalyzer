
let gLangEn = 1;
let gLangDe = 2;

let gCurLang = gLangEn;

let translations = [
    // HTML element ID  English (1)  German (2)

    // Navigation bar
    ["navbar_dropdown_language", "Language", "Sprache"],

    // Side bar
    ["sidebar_headline_overview", "Overview", "Übersicht"],
    ["sidebar_today", "Today", "Heute"],
    ["sidebar_statistics", "Statistics", "Statistiken"],
    ["sidebar_headline_history", "History", "Historie"],
    ["sidebar_by_day", "By Day", "Nach Tag"],
    ["sidebar_by_month", "By Month", "Nach Monat"],
    ["sidebar_by_year", "By Year", "Nach Jahr"],
    ["sidebar_all_time", "All Time", "Gesamt"],
    ["sidebar_headline_misc", "Misc", "Sonstiges"],
    ["sidebar_csv", "CSV Download", "CSV-Download"],

    // Statistics
    ["headline_statistics", "Statistics", "Statistiken"],
    ["stats_card_highest_prod", "Highest Production", "Höchste Erzeugung"],
    ["stats_card_best_day", "Best Day", "Bester Tag"],
    ["stats_card_best_month", "Best Month", "Bester Monat"],
    ["stats_card_best_year", "Best Year", "Bestes Jahr"],
    ["stats_card_averages", "Averages ", "Durchschnittswerte"],
    ["stats_card_runtime", "Runtime ", "Laufzeit"],
    ["statistics_text_avg_daily_prod", "Average daily production ", "Durchschn. täglich erzeugt"],
    ["statistics_text_start_date", "Date of commissioning ", "Inbetriebnahme der Anlage"],
    ["statistics_text_runtime", "Total runtime ", "Laufzeit der Anlage"],

    // Dashboard
    ["dashboard_subtitle", "Last updated: ", "Letzte Aktualisierung: "],

    ["dash_card_current", "Current", "Momentanwerte"],
    ["dash_card_today", "Today", "Heutige Werte"],
    ["dash_card_all_time", "All Time", "Allzeit-Werte"],
    ["dash_card_24h", "Short Term History", "Aktueller Verlauf"],

    ["dash_text_today_produced", "Produced today", "Heute erzeugt"],
    ["dash_text_today_consumed", "Consumed today", "Heute verbraucht"],
    ["dash_text_today_fed_in", "Fed in today", "Heute eingespeist"],
    ["dash_text_today_autarky", "Today's autarky", "Heutige Autarkie"],
    ["dash_text_today_earned", "Earned today", "Heute verdient"],

    ["dash_text_all_time_produced", "Produced in total", "Insgesamt erzeugt"],
    ["dash_text_all_time_consumed", "Consumed in total", "Insgesamt verbraucht"],
    ["dash_text_all_time_fed_in", "Fed in total", "Insgesamt eingespeist"],
    ["dash_text_all_time_autarky", "Average autarky", "Durchschn. Autarkie"],
    ["dash_text_all_time_earned", "Earned in total", "Insgesamt verdient"],

    // History
    ["history_card_earned", "Earnings", "Einnahmen"],
    ["history_card_usage", "Produced", "Erzeugt"],
    ["history_card_consumption", "Consumed", "Verbraucht"],
    ["history_text_produced", "Energy produced", "Erzeugte PV-Energie"],
    ["history_text_earned_feedin", "Earned with feed-in", "Verdienst durch Einspeisung"],
    ["history_text_earned_self", "Saved via self-consumption", "Ersparnis durch Eigenverbrauch"],
    ["history_text_earned_total", "Total", "Summe"],
    ["history_text_fedin", "Fed into the grid", "Ins Netz eingespeist"],
    ["history_text_self_consumed", "Self consumed", "Selbst verbraucht"],
    ["history_text_consumption_grid", "Consumption from grid", "Verbrauch aus dem Netz"],
    ["history_text_consumption_self", "Consumption from PV", "Verbrauch aus PV"],
    ["history_text_consumption_total", "Total consumption", "Gesamtverbrauch"],
    ["history_card_graph_production_text", "Production Details", "Zeitverlauf der Erzeugung"],
    ["history_card_graph_consumption_text", "Consumption Details", "Zeitverlauf des Verbrauchs"],
    ["history_card_autarky", "Autarky", "Autarkie"],
    ["history_text_autarky", "Achieved autarky", "Erreichte Autarkie"],
    ["history_card_high_res_data_text", "Course of the Day", "Tagesverlauf"],

    // CSV download
    ["csv_subtitle", "Download .csv reports ", "Report-Dateien im .csv-Format herunterladen"],
    ["csv_label_time_range", "Time range:", "Zeitraum:"],
    ["csv_label_resolution", "Resolution:", "Granularität:"],
    ["csv_range_rad_lbl_day", "A single day", "Ein Tag"],
    ["csv_range_rad_lbl_month", "A month", "Ein Monat"],
    ["csv_range_rad_lbl_year", "A year", "Ein jahr"],
    ["csv_range_rad_lbl_all", "All time", "Alles"],
    ["csv_res_rad_lbl_day", "Single days", "Einzelne Tage"],
    ["csv_res_rad_lbl_month", "Summed up by months", "Auf Monate summiert"],
    ["csv_res_rad_lbl_year", "Summed up by years", "Auf Jahre summiert"],

    // Months combo box
    ["cbx_month_1", "January", "Januar"],
    ["cbx_month_2", "February", "Februar"],
    ["cbx_month_3", "March", "März"],
    ["cbx_month_4", "April", "April"],
    ["cbx_month_5", "May", "Mai"],
    ["cbx_month_6", "June", "Juni"],
    ["cbx_month_7", "July", "Juli"],
    ["cbx_month_8", "August", "August"],
    ["cbx_month_9", "September", "September"],
    ["cbx_month_10", "October", "Oktober"],
    ["cbx_month_11", "November", "November"],
    ["cbx_month_12", "December", "Dezember"],

    // Months combo box
    ["csv_cbx_month_1", "January", "Januar"],
    ["csv_cbx_month_2", "February", "Februar"],
    ["csv_cbx_month_3", "March", "März"],
    ["csv_cbx_month_4", "April", "April"],
    ["csv_cbx_month_5", "May", "Mai"],
    ["csv_cbx_month_6", "June", "Juni"],
    ["csv_cbx_month_7", "July", "Juli"],
    ["csv_cbx_month_8", "August", "August"],
    ["csv_cbx_month_9", "September", "September"],
    ["csv_cbx_month_10", "October", "Oktober"],
    ["csv_cbx_month_11", "November", "November"],
    ["csv_cbx_month_12", "December", "Dezember"],

    // Info
    ["info_no_data", "No data is available for the selected time span.", "Für den gewählten Zeitraum liegen keine Daten vor."],
];

let chartStrings = [
    // HTML element ID          English (1)             German (2)
    ["chart_produced_w", "Production", "Erzeugung"],
    ["chart_consumed_w", "Consumption", "Verbrauch"],
    ["chart_fed_in_w", "Feed-in", "Einspeisung"],
    ["chart_from_grid", "From grid", "Aus dem Netz"],
    ["chart_from_pv", "From PV", "Aus PV"],
    ["chart_produced", "Produced", "Erzeugt"],
    ["chart_consumed", "Consumed", "Verbraucht"],
    ["chart_fed_in", "Fed in", "Eingespeist"],
    ["chart_self_consumed", "Self consumed", "Eigenverbrauch"],
    ["chart_produced_self_kwh", "Consumed directly", "Direktverbrauch"],
    ["chart_produced_grid_kwh", "Feed-in", "Einspeisung"],
    ["chart_consumed_pv_kwh", "From PV", "Aus PV"],
    ["chart_consumed_grid_kwh", "From grid", "Netzbezug"],
    ["chart_total", "Total", "Gesamt"],
];

let historyStrings = [
    // HTML element ID      English (1)             German (2)
    ["daily_data", "Daily Data", "Daten nach Tag"],
    ["monthly_data", "Monthly Data", "Daten nach Monat"],
    ["yearly_data", "Yearly Data", "Daten nach Jahr"],
    ["all_time_data", "All Time Data", "Allzeitdaten"],
];


function restoreLanguage() {
    var lang = localStorage.getItem("lang");
    if (lang != null)
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
        try {
            document.getElementById(translation[0]).innerHTML = translation[index];
        } catch (error) {
            console.error("Could not localize element " + translation[0] + ": " + error);
        }
    });
}

function getChartString(id) {
    for (i = 0; i < chartStrings.length; ++i)
        if (chartStrings[i][0] == id)
            return chartStrings[i][gCurLang];
    return "...";
}

function getHistoryString(id) {
    for (i = 0; i < historyStrings.length; ++i)
        if (historyStrings[i][0] == id)
            return historyStrings[i][gCurLang];
    return "...";
}


// Number format with 2 decimals
const format2_en = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

// Number format with 0 decimals
const format0_en = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
});

// Number format with 2 decimals
const format2_de = new Intl.NumberFormat('de-DE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

// Number format with 0 decimals
const format0_de = new Intl.NumberFormat('de-DE', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
});

function numFormat(number, digits) {
    if (digits == 2) {
        if (gCurLang == gLangDe)
            return format2_de.format(number);
        else
            return format2_en.format(number);
    }
    else {
        if (gCurLang == gLangDe)
            return format0_de.format(number);
        else
            return format0_en.format(number);
    }
}


let monthNames = [
    // English (1), German (2)
    ["January", "Januar"],
    ["February", "Februar"],
    ["March", "März"],
    ["April", "April"],
    ["May", "Mai"],
    ["June", "Juni"],
    ["July", "Juli"],
    ["August", "August"],
    ["September", "September"],
    ["October", "Oktober"],
    ["November", "November"],
    ["December", "Dezember"],
];

function getMonthName(index) {
    return monthNames[index][gCurLang - 1];
}

function getLocale() {
    return gCurLang == gLangDe ? "de" : "en";
}

function getUnitDays() {
    return gCurLang == gLangDe ? "Tage" : "days";
}

function prettyPrintDateString(date) {
    var d = new Date(date)
    let localeDate = d.toLocaleString(getLocale(), {
        weekday: "long",
        day: "numeric",
        year: "numeric",
        month: "long",
    });
    return localeDate;
}

function prettyPrintDateStringWithoutDay(date) {
    var d = new Date(date)
    let localeDate = d.toLocaleString(getLocale(), {
        year: "numeric",
        month: "long",
    });
    return localeDate;
}