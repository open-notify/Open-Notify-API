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

L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
}).addTo(map);

var iss = L.marker([0, 0]).addTo(map)

moveISS();
