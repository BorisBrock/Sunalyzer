// Opens a link to download a .csv file from the server
function downloadCsv() {
    // Get the table
    let table = "days";
    if (document.getElementById("csv_res_rad_month").checked == true)
        table = "months";
    else if (document.getElementById("csv_res_rad_year").checked == true)
        table = "years";

    // Get the date
    let year = document.getElementById('csv_selection_year2').value.toString();
    let month = padStr(document.getElementById('csv_selection_month2').value.toString());
    let day = padStr(document.getElementById('csv_selection_day2').value.toString());

    let date = "";
    if (document.getElementById("csv_range_rad_all").checked == true)
        date = "";
    else if (document.getElementById("csv_range_rad_year").checked == true)
        date = year;
    else if (document.getElementById("csv_range_rad_month").checked == true)
        date = year + "-" + month;
    else if (document.getElementById("csv_range_rad_day").checked == true)
        date = year + "-" + month + "-" + day;

    // Buildquery
    url = document.baseURI + "/csv?table=" + table;
    if (date.length > 0)
        url += "&date=" + date;

    console.log("Executing CSV query: " + url);
    window.open(url);
}
