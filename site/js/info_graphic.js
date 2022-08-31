paper.install(window);
window.addEventListener('DOMContentLoaded', event => {
    paper.setup("dashboard_info_graphic");

    var path = new Path();
    path.add(new Point(0,0));
    path.add(new Point(240,240));
    path.strokeColor = "black";

    var path2 = new Path();
    path2.add(new Point(0,240));
    path2.add(new Point(240,0));
    path2.strokeColor = "red";

    var rect = new Path.Rectangle({
        point: [0, 0],
        size: [view.size.width, view.size.height],
        selected: true
    });
    rect.sendToBack();
    rect.fillColor = '#00FF00';
});