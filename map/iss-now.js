var map = L.map('map').setView([0,0], 2);


function moveISS () {
    $.getJSON('http://api.open-notify.org/iss-now.json?callback=?', function(data) {
        var lat = data['iss_position']['latitude'];
        var lon = data['iss_position']['longitude'];

        iss.setLatLng([lat, lon]);
        isscirc.setLatLng([lat, lon]);
        map.panTo([lat, lon], animate=true);
    });
    setTimeout(moveISS, 5000); 
}

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


var iss = L.marker([0, 0], {icon: ISSIcon}).addTo(map);
var isscirc = L.circle([0,0], 2200e3, {color: "#c22", opacity: 0.3, weight:1, fillColor: "#c22", fillOpacity: 0.1}).addTo(map); 

moveISS();
