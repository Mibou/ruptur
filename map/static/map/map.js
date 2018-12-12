
String.prototype.format = function () {
  var args = arguments;
  return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
    if (m == "{{") { return "{"; }
    if (m == "}}") { return "}"; }
    return args[n];
  });
};

var allMarkers = []
var map = L.map('map').setView([46.871170, -1.013180], 9);
var pois = []

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Tiles Courtesy of <a href="https://www.openstreetmap.org/" target="_blank">Open street map</a> — Map data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 18,
  minZoom: 2,
  reuseTiles: true,
  subdomains: 'abc',
}).addTo(map);
map.removeControl(map.zoomControl);

function updatePois() {
  $.each(allMarkers, function(index, marker) { marker.remove() });

  bounds = map.getBounds();
  bottom_left = bounds.getSouthWest();
  top_right = bounds.getNorthEast();
  bl_lat = bottom_left.lat;
  bl_lon= bottom_left.lng;
  tr_lat= top_right.lat;
  tr_lon= top_right.lng;

  $.ajax({
    url: '/api/v1/poi/?format=json',
    contentType: 'application/json',
    type: 'GET',
    async: false,
    data: {
      "bl_lat": bottom_left.lat,
      "bl_lon": bottom_left.lng,
      "tr_lat": top_right.lat,
      "tr_lon": top_right.lng
    },
    success: function(data) {
      $('#filter').html('');
      pois = data.objects
      pois.forEach(function(poi) {
        $('#filter').append(generateInfoDiv(poi))
        currentMarker = L.marker(
          [poi.latitude, poi.longitude], {
          clickable: true
        })
        currentMarker.addTo(map);
        allMarkers.push(currentMarker);
      });
    }
  });
}

function generateInfoDiv(poi) {
  poiTags = '';
  poi.tags.forEach(function(poiTag) { poiTags = poiTags + '<div class="poiContentTag">#{0}</div>'.format(poiTag); });
  return '<a id="{0}" href="{5}" class="link-magasin" title="{2}"><div class="poiListItem"><div class="poiIconWrapper"><div class="poiIcon"><i class="poiIcon fa fa-{1}"></i></div></div><div class="poiContent"><div class="poiContentTitle" title="{2}">{2}</div><div class="poiContentSubtitle" title="{3}">{3}</div><div class="poiContentTags">{4}</div></div></div></a>'.format(poi.id, poi.icon, poi.title, poi.subtitle, poiTags, poi.url);
}

$(document).on("click", ".link-magasin", function(){
  index = pois.findIndex(poi => poi.id == this.id);
  poi = pois[index];
  Lat_Lng = new L.LatLng(poi.latitude, poi.longitude);
  map.setView(Lat_Lng , 15, {pan: {animate:true, duration: 1}});
});

updatePois();

map.on("moveend", function (e) {
  updatePois();
});
