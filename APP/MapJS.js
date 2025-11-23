ymaps.ready(init);
function init(){
    var myMap = new ymaps.Map ('app', {
        center: [55.75, 37.61],
        zoom: 10
    });

    var myPolygon = new ymaps.Polygon([[
        [55.778607,37.553126],
        [55.792923,37.647883],
        [55.724391,37.709681],
        [55.708887,37.583339]
    ]]);
    myMap.geoObjects.add(myPolygon);
}