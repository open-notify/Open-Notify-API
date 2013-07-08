var map = L.map('map').setView([0,0], 2);


function moveISS () {
    $.getJSON('http://open-notify-api.herokuapp.com/iss-now.json?callback=?', function(data) {
        var lat = data['data']['iss_position']['latitude'];
        var lon = data['data']['iss_position']['longitude'];

        iss.setLatLng([lat, lon]);
        map.panTo([lat, lon], animate=true);
    });
    setTimeout(moveISS, 5000); 
}

// /Open-Notify-API/map/tiles/4/14/13.png
//L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
L.tileLayer('/Open-Notify-API/map/tiles/{z}/{x}/{y}.png', {
    maxZoom: 4,
}).addTo(map);

var ISSIcon = L.icon({
    iconUrl: '/Open-Notify-API/map/ISSIcon.png',
    iconSize: [50, 30],
    iconAnchor: [25, 15],
    popupAnchor: [50, 25],
    shadowUrl: '/Open-Notify-API/map/ISSIcon_shadow.png',
    shadowSize: [60, 40],
    shadowAnchor: [30, 15]
});


var iss = L.marker([0, 0], {icon: ISSIcon}).addTo(map)

moveISS();
