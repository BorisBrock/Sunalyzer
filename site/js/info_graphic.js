var gAnimation;
var gShowPvToGrid = false;
var gShowPvToHome = false;
var gShowGridToHome = false;

window.onload = function start() {

    updateInfoGraphic(0, 0, 0);
    gAnimation = setInterval(animateInfoGraphic, 1000);

 }

 function animateInfoGraphic() {
    // PV to grid
    if (gShowPvToGrid) {
       animate("dot_pv_grid_1", 150);
       animate("dot_pv_grid_2", 100);
       animate("dot_pv_grid_3", 50);
       animate("dot_pv_grid_4", 0);
    }
    else {
       SVG('#dot_pv_grid_1').opacity(0.0);
       SVG('#dot_pv_grid_2').opacity(0.0);
       SVG('#dot_pv_grid_3').opacity(0.0);
       SVG('#dot_pv_grid_4').opacity(0.0);
       SVG('#txt_pv_grid').opacity(0.0);
    }

    // Grid to home
    if (gShowGridToHome) {
       animate("dot_grid_home_1", 0);
       animate("dot_grid_home_2", 50);
       animate("dot_grid_home_3", 100);
       animate("dot_grid_home_4", 150);
    }
    else {
       SVG('#dot_grid_home_1').opacity(0.0);
       SVG('#dot_grid_home_2').opacity(0.0);
       SVG('#dot_grid_home_3').opacity(0.0);
       SVG('#dot_grid_home_4').opacity(0.0);
       SVG('#txt_grid_home').opacity(0.0);
    }

    // PV to home
    if (gShowPvToHome) {
       animate("dot_pv_home_1", 0);
       animate("dot_pv_home_2", 50);
       animate("dot_pv_home_3", 100);
       animate("dot_pv_home_4", 150);
    }
    else {
       SVG('#dot_pv_home_1').opacity(0.0);
       SVG('#dot_pv_home_2').opacity(0.0);
       SVG('#dot_pv_home_3').opacity(0.0);
       SVG('#dot_pv_home_4').opacity(0.0);
       SVG('#txt_pv_home').opacity(0.0);
    }
 }

 function animate(name, delay) {
    SVG('#' + name).opacity(0.3).delay(delay).animate(40).opacity(1.0).animate(400).opacity(0.3);
 }


 function updateInfoGraphic(generatedWh, gridConsumptionWh, fedInWh) {
    // PV to grid
    if (fedInWh > 0) {
       gShowPvToGrid = true;
       SVG('#txt_pv_grid').opacity(1.0);
       document.getElementById('txt_pv_grid').textContent = fedInWh.toString() + " Wh";
    }
    else {
       gShowPvToGrid = false;
    }

    // Grid to home
    if (gridConsumptionWh > 0) {
       gShowGridToHome = true;
       SVG('#txt_grid_home').opacity(1.0);
       document.getElementById('txt_grid_home').textContent = gridConsumptionWh.toString();
    }
    else {
       gShowGridToHome = false;
    }

    // PV to home
    let pvConsumptionWh = generatedWh - fedInWh;
    if (pvConsumptionWh > 0) {
       gShowPvToHome = true;
       SVG('#txt_pv_home').opacity(1.0);
       document.getElementById('txt_pv_home').textContent = pvConsumptionWh.toString();
    }
    else {
       gShowPvToHome = false;
    }
 }