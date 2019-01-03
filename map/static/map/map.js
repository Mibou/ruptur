
String.prototype.format = function () {
  var args = arguments;
  return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, n) {
    if (m == "{{") { return "{"; }
    if (m == "}}") { return "}"; }
    return args[n];
  });
};

function savePosition(position) {
  $('#user-lat').val(position.coords.latitude);
  $('#user-lon').val(position.coords.longitude);

  if ($('#user-lat').val() != "" && $('user-lon').val() != "") {
    map.panTo([parseFloat($('#user-lat').val()), parseFloat($('#user-lon').val())]);
  }

  updatePois();
}

function geolocationBlocked() {
  $(document).trigger("add-alerts", [{
    "message": "Vous n'avez pas autorisé la <strong>géolocalisation</strong> ! Autorisez la géolocation et rechargez la page !",
    "priority": "danger"
  }]);
}
function geolocationFailed() {
  $(document).trigger("add-alerts", [{
    "message": "Nous n'avons pas réussi à vous <strong>géolocaliser</strong> ! Essayez d'autres méthodes de recherche !",
    "priority": "danger"
  }]);
}

function locationFailure(error) {
  if (error.code == error.PERMISSION_DENIED)
    geolocationBlocked();
  else
    geolocationFailed();
}

function getLocation() {
  if (navigator.geolocation)
    navigator.geolocation.getCurrentPosition(savePosition, locationFailure);
  else
    geolocationFailed();
}

$(document).on("click", ".around-me", function(){
  getLocation();
});

var allMarkers = []

var map = L.map('map', {
  center: [46.871170, -1.013180],
  zoom: 9,
  zoomControl: true
});

L.control.zoom({
  position: 'topright',
  zoomInText: '+',
  zoomOutText: '-'
}).addTo(map);

var pois = []
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Tiles Courtesy of <a href="https://www.openstreetmap.org/" target="_blank">Open street map</a> — Map data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 11,
  minZoom: 4,
  reuseTiles: true,
  subdomains: 'abc',
}).addTo(map);
map.removeControl(map.zoomControl);

function updatePois() {
  $.each(allMarkers, function(index, marker) { marker.remove() });
  $('#filter').infiniteScrollHelper('destroy');
  $('#filter').html('');
  setInfiniteScroll();
}

function getPois(page, done) {
  skills = $('#skillsCheck').is(':checked');
  projects = $('#projectsCheck').is(':checked');
  ideas = $('#ideasCheck').is(':checked');

  bounds = map.getBounds();
  bottom_left = bounds.getSouthWest();
  top_right = bounds.getNorthEast();
  bl_lat = bottom_left.lat;
  bl_lon= bottom_left.lng;
  tr_lat= top_right.lat;
  tr_lon= top_right.lng;

  if(page==undefined)
    page = 1

  $.ajax({
    url: '/api/v1/poi/?format=json&page='+page,
    contentType: 'application/json',
    type: 'GET',
    async: false,
    data: {
      "lat": $('#user-lat').val(),
      "lon": $('#user-lon').val(),
      "bl_lat": bottom_left.lat,
      "bl_lon": bottom_left.lng,
      "tr_lat": top_right.lat,
      "tr_lon": top_right.lng,
      "skills": skills,
      "projects": projects,
      "ideas": ideas,
      "search": $('#searchText').val()
    },
    success: function(data) {

      if(data['meta']['next'] == false) {
        $('#filter').infiniteScrollHelper('destroy');
      }

      pois = data.objects
      pois.forEach(function(poi) {
        $('#filter').append(generateInfoDiv(poi))
        currentMarker = L.marker(
          [poi.latitude, poi.longitude],
          { clickable: true }
        );
        currentMarker.addTo(map);
        allMarkers.push(currentMarker);
      });

      done();
    }
  });
}

function setInfiniteScroll() {
  $('#filter').infiniteScrollHelper({
    startingPageCount: 0,
    loadMore: function(page, done) {
      // load some data, parse some data
      getPois(page, done);
    },
    doneLoading: function() {
      return false;
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

$(document).on("keyup", "#searchText", updatePois);
$(document).on("click", ".custom-control-input", updatePois);

updatePois();

map.on("moveend", function (e) {
  updatePois();
});

$(document).ready(function () {
  $(".ui-layout-west").resizable({
      handleSelector: ".splitter",
      resizeHeight: false
  });
});