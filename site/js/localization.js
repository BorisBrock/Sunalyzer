
let gLangEn = 1;
let gLangDe = 2;
let gLangFr = 3;

let gCurLang = gLangEn;

let translations = [
    // HTML element ID  English (1)  German (2) French (3)

    // Navigation bar
    ["navbar_dropdown_language", "Language", "Sprache", "Langue"],

    // Side bar
    ["sidebar_headline_overview", "Overview", "Übersicht", "Aperçu"],
    ["sidebar_today", "Today", "Heute", "Aujourd'hui"],
    ["sidebar_statistics", "Statistics", "Statistiken", "Statistiques"],
    ["sidebar_dashboard", "Dashboard", "Armaturenbrett", "Tableau de bord"],
    ["sidebar_headline_history", "History", "Historie", "Historique"],
    ["sidebar_by_day", "By Day", "Nach Tag", "Journalier"],
    ["sidebar_by_month", "By Month", "Nach Monat", "Mensuel"],
    ["sidebar_by_year", "By Year", "Nach Jahr", "Annuel"],
    ["sidebar_all_time", "All Time", "Gesamt", "Global"],
    ["sidebar_headline_misc", "Misc", "Sonstiges", "Outils"],
    ["sidebar_csv", "CSV Download", "CSV-Download", "Export CSV"],

    // Statistics
    ["headline_statistics", "Statistics", "Statistiken", "Statistiques"],
    ["stats_card_highest_prod", "Highest Production", "Höchste Erzeugung", "Production maximale"],
    ["stats_card_best_day", "Best Day", "Bester Tag", "Meilleure journée"],
    ["stats_card_best_month", "Best Month", "Bester Monat", "Meilleur mois"],
    ["stats_card_best_year", "Best Year", "Bestes Jahr", "Meilleure année"],
    ["stats_card_averages", "Averages ", "Durchschnittswerte", "Moyennes"],
    ["stats_card_runtime", "Runtime ", "Laufzeit", "Temps de fonctionnement"],
    ["statistics_text_avg_daily_prod", "Average daily production ", "Durchschn. täglich erzeugt", "Production journalière moyenne"],
    ["statistics_text_start_date", "Date of commissioning ", "Inbetriebnahme der Anlage", "Date d'initialisation"],
    ["statistics_text_runtime", "Total runtime ", "Laufzeit der Anlage", "Durée totale"],

    // Dashboard
    ["headline_dashboard", "Dashboard", "Armaturenbrett", "Tableau de bord"],
    ["dashboard_subtitle", "Last updated: ", "Letzte Aktualisierung: ", "Actualisation: "],

    ["dash_card_current", "Current", "Momentanwerte", "Maintenant"],
    ["dash_card_today", "Today", "Heutige Werte", "Aujourd'hui"],
    ["dash_card_all_time", "All Time", "Allzeit-Werte", "Total"],
    ["dash_card_24h", "Short Term History", "Aktueller Verlauf", "Dernières heures"],

    ["dash_text_today_produced", "Produced today", "Heute erzeugt", "Production du jour"],
    ["dash_text_today_consumed", "Consumed today", "Heute verbraucht", "Consommation du jour"],
    ["dash_text_today_fed_in", "Fed in today", "Heute eingespeist", "Injection du jour"],
    ["dash_text_today_autarky", "Today's autarky", "Heutige Autarkie", "Autonomie du jour"],
    ["dash_text_today_earned", "Earned today", "Heute verdient", "Gain du jour"],

    ["dash_text_all_time_produced", "Produced in total", "Insgesamt erzeugt", "Production totale"],
    ["dash_text_all_time_consumed", "Consumed in total", "Insgesamt verbraucht", "Consommation totale"],
    ["dash_text_all_time_fed_in", "Fed in total", "Insgesamt eingespeist", "Injection totale"],
    ["dash_text_all_time_autarky", "Average autarky", "Durchschn. Autarkie", "Autonomie moyenne"],
    ["dash_text_all_time_earned", "Earned in total", "Insgesamt verdient", "Gain total"],

    // History
    ["history_card_earned", "Earnings", "Einnahmen", "Gains"],
    ["history_card_usage", "Produced", "Erzeugt", "Production"],
    ["history_card_consumption", "Consumed", "Verbraucht", "Consommation"],
    ["history_text_produced", "Energy produced", "Erzeugte PV-Energie", "Energie produite"],
    ["history_text_earned_feedin", "Earned with feed-in", "Verdienst durch Einspeisung", "Gain d'injection"],
    ["history_text_earned_self", "Saved via self-consumption", "Ersparnis durch Eigenverbrauch", "Gain d'autoconsommation"],
    ["history_text_earned_total", "Total", "Summe", "Total"],
    ["history_text_fedin", "Fed into the grid", "Ins Netz eingespeist", "Injection vers le réseau"],
    ["history_text_self_consumed", "Self consumed", "Selbst verbraucht", "Autoconsommé"],
    ["history_text_consumption_grid", "Consumption from grid", "Verbrauch aus dem Netz", "Consommation du réseau"],
    ["history_text_consumption_self", "Consumption from PV", "Verbrauch aus PV", "Consommation solaire"],
    ["history_text_consumption_total", "Total consumption", "Gesamtverbrauch", "Consommation totale"],
    ["history_card_graph_production_text", "Production Details", "Zeitverlauf der Erzeugung", "Détail de production"],
    ["history_card_graph_consumption_text", "Consumption Details", "Zeitverlauf des Verbrauchs", "Détail de consommation"],
    ["history_card_autarky", "Autarky", "Autarkie", "Autonomie"],
    ["history_text_autarky", "Achieved autarky", "Erreichte Autarkie", "Autonomie atteinte"],
    ["history_card_high_res_data_text", "Course of the Day", "Tagesverlauf", "Déroulement de la journée"],

    // CSV download
    ["csv_subtitle", "Download .csv reports ", "Report-Dateien im .csv-Format herunterladen", "Télécharger le rapport CSV"],
    ["csv_label_time_range", "Time range:", "Zeitraum:", "Période:"],
    ["csv_label_resolution", "Resolution:", "Granularität:", "Découpage:"],
    ["csv_range_rad_lbl_day", "A single day", "Ein Tag","Jour"],
    ["csv_range_rad_lbl_month", "A month", "Ein Monat", "Mois"],
    ["csv_range_rad_lbl_year", "A year", "Ein jahr", "Année"],
    ["csv_range_rad_lbl_all", "All time", "Alles", "Tout"],
    ["csv_res_rad_lbl_day", "Single days", "Einzelne Tage", "Par jour"],
    ["csv_res_rad_lbl_month", "Summed up by months", "Auf Monate summiert", "Par mois"],
    ["csv_res_rad_lbl_year", "Summed up by years", "Auf Jahre summiert", "Par année"],

    // Months combo box
    ["cbx_month_1", "January", "Januar", "Janvier"],
    ["cbx_month_2", "February", "Februar", "Février"],
    ["cbx_month_3", "March", "März", "Mars"],
    ["cbx_month_4", "April", "April", "Avril"],
    ["cbx_month_5", "May", "Mai", "Mai"],
    ["cbx_month_6", "June", "Juni", "Juin"],
    ["cbx_month_7", "July", "Juli", "Juillet"],
    ["cbx_month_8", "August", "August", "Août"],
    ["cbx_month_9", "September", "September", "Septembre"],
    ["cbx_month_10", "October", "Oktober", "Octobre"],
    ["cbx_month_11", "November", "November", "Novembre"],
    ["cbx_month_12", "December", "Dezember", "Décembre"],

    // Months combo box
    ["csv_cbx_month_1", "January", "Januar", "Janvier"],
    ["csv_cbx_month_2", "February", "Februar", "Février"],
    ["csv_cbx_month_3", "March", "März", "Mars"],
    ["csv_cbx_month_4", "April", "April", "Avril"],
    ["csv_cbx_month_5", "May", "Mai", "Mai"],
    ["csv_cbx_month_6", "June", "Juni", "Juin"],
    ["csv_cbx_month_7", "July", "Juli", "Juillet"],
    ["csv_cbx_month_8", "August", "August", "Août"],
    ["csv_cbx_month_9", "September", "September", "Septembre"],
    ["csv_cbx_month_10", "October", "Oktober", "Octobre"],
    ["csv_cbx_month_11", "November", "November", "Novembre"],
    ["csv_cbx_month_12", "December", "Dezember", "Décembre"],

    // Info
    ["info_no_data", "No data is available for the selected time span.", "Für den gewählten Zeitraum liegen keine Daten vor.", "Aucune donnée disponible pour la période sélectionnée"],
];

let chartStrings = [
    // HTML element ID          English (1)             German (2)  French (3)
    ["chart_produced_w", "Production", "Erzeugung", "Production"],
    ["chart_consumed_w", "Consumption", "Verbrauch", "Consommation"],
    ["chart_fed_in_w", "Feed-in", "Einspeisung", "Injection"],
    ["chart_from_grid", "From grid", "Aus dem Netz", "Consommation du réseau"],
    ["chart_from_pv", "From PV", "Aus PV", "Consommation solaire"],
    ["chart_produced", "Produced", "Erzeugt", "Produite"],
    ["chart_consumed", "Consumed", "Verbraucht", "Consommé"],
    ["chart_fed_in", "Fed in", "Eingespeist", "Injecté"],
    ["chart_self_consumed", "Self consumed", "Eigenverbrauch", "Autoconsommée"],
    ["chart_produced_self_kwh", "Consumed directly", "Direktverbrauch", "Consommé directement"],
    ["chart_produced_grid_kwh", "Feed-in", "Einspeisung", "Injection"],
    ["chart_consumed_pv_kwh", "From PV", "Aus PV", "Consomation solaire"],
    ["chart_consumed_grid_kwh", "From grid", "Netzbezug", "Consommation du réseau"],
    ["chart_total", "Total", "Gesamt", "Total"],
];

let historyStrings = [
    // HTML element ID      English (1)             German (2)    French (3)
    ["daily_data", "Daily Data", "Daten nach Tag", "Données journalières"],
    ["monthly_data", "Monthly Data", "Daten nach Monat", "Données mensuelle"],
    ["yearly_data", "Yearly Data", "Daten nach Jahr", "Données annuelles"],
    ["all_time_data", "All Time Data", "Allzeitdaten", "Données globales"],
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

function switchLanguageToFrench() {
    switchLanguageByIndex(gLangFr);
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

// Number format with 2 decimals
const format2_fr = new Intl.NumberFormat('fr-FR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

// Number format with 0 decimals
const format0_fr = new Intl.NumberFormat('fr-FR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
});

function numFormat(number, digits) {
    if (digits == 2) {
        if (gCurLang == gLangDe)
            return format2_de.format(number);
        else if (gCurLang == gLangFr)
            return format2_fr.format(number);
        else
            return format2_en.format(number);
    }
    else {
        if (gCurLang == gLangDe)
            return format0_de.format(number);
        else if (gCurLang == gLangFr)
            return format0_fr.format(number);
        else
            return format0_en.format(number);
    }
}


let monthNames = [
    // English (1), German (2), French (3)
    ["January", "Januar", "Janvier"],
    ["February", "Februar", "Février"],
    ["March", "März", "Mars"],
    ["April", "April", "Avril"],
    ["May", "Mai", "Mai"],
    ["June", "Juni", "Juin"],
    ["July", "Juli", "Juillet"],
    ["August", "August", "Août"],
    ["September", "September", "Septembre"],
    ["October", "Oktober", "Octobre"],
    ["November", "November", "Novembre"],
    ["December", "Dezember", "Décembre"],
];

function getMonthName(index) {
    return monthNames[index][gCurLang - 1];
}

function getLocale() {
    return gCurLang == gLangDe ? "de" : (gCurLang == gLangFr ? "fr" : "en");
}

function getUnitDays() {
    return gCurLang == gLangDe ? "Tage" : (gCurLang == gLangFr ? "jours" : "days");
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