
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
  pois = [
    {id: 1, type:'user', title: 'Alain DURET', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.8711, -1.0131]},
    {id: 2, type:'user', title: 'Marie COUTANCEAU', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.6705, -1.4264]},
    {id: 3, type:'rocket', title: 'Agroécologie Urbaine', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.6978, -1.9445]},
    {id: 4, type:'lightbulb', title: 'Obsolescence programmée', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.4930, -1.7955]},
    {id: 5, type:'lightbulb', title: 'Recherche 300kg de carton', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [47.2184, -1.5536]},
    {id: 6, type:'user', title: 'Pascal METENIER', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.4660, -0.8065]},
    {id: 7, type:'user', title: 'Alain DURET', subtitle: 'Immobilier', tags: ['Recyclage déchets','Energies renouvelables'], coordinates: [46.9949, -1.7399]}
  ]

  $('#filter').html('');
  pois.forEach(function(poi) {
    $('#filter').append(generateInfoDiv(poi))
    currentMarker = L.marker(
      poi.coordinates, {
      clickable: true
    })
    currentMarker.addTo(map);
    allMarkers.push(currentMarker);
  });

}

function generateInfoDiv(poi) {
  poiTags = '';
  poi.tags.forEach(function(poiTag) { poiTags = poiTags + '<div class="poiContentTag">#{0}</div>'.format(poiTag); });
  return '<a id="{0}" class="link-magasin" title="{2}"><div class="poiListItem"><div class="poiIconWrapper"><div class="poiIcon"><i class="poiIcon fa fa-{1}"></i></div></div><div class="poiContent"><div class="poiContentTitle">{2}</div><div class="poiContentSubtitle">{3}</div><div class="poiContentTags">{4}</div></div></div></a>'.format(poi.id, poi.type, poi.title, poi.subtitle, poiTags);
}

$(document).on("click", ".link-magasin", function(){
  index = pois.findIndex(poi => poi.id == this.id);
  poi = pois[index];
  Lat_Lng = new L.LatLng(poi['coordinates'][0], poi['coordinates'][1]);
  map.setView(Lat_Lng , 15, {pan: {animate:true, duration: 1}});
});

updatePois();

map.on("moveend", function (e) {
  updatePois();
  /*
  var objects = [];
  zoom = map.getZoom();
  bounds = map.getBounds();
  bottom_left = bounds.getSouthWest();
  top_right = bounds.getNorthEast();
  bl_lat = bottom_left.lat;
  bl_lon= bottom_left.lng;
  tr_lat= top_right.lat;
  tr_lon= top_right.lng;
  if ( zoom >= 14 ) {
     $('.modal-body').show();
     $.ajax({
      url: '/api/v1/magasins/{{latitude}}/{{longitude}}/'+bl_lat+'/'+bl_lon+'/'+tr_lat+'/'+tr_lon+'/web/?format=json',
      type: 'GET',
      data: {
      },
      success: function(data) {
        $('.modal-body').hide();
        objects = data.objects;

        //adding non partenaires
        for (var id in objects) {

          lat = parseFloat(objects[id].latitude);
          lng = parseFloat(objects[id].longitude);

          if (!nonPartenaires.hasOwnProperty(objects[id].id)) {
            var markerNon = L.marker(
            [lat, lng],
            {
              icon: new L.icon({
                iconUrl: "{{ STATIC_URL }}markers/images/green-icon.png",
                iconSize:     [21, 23],
                popupSize:    [250, 56],
                iconAnchor:   [0, 12], // point of the icon which will correspond to marker's location
                popupAnchor:  [6, -12] // point from which the popup should open relative to the iconAnchor
              })
            });
            markerNon.idMagasin = objects[id].id;
            total_votes = objects[id].votes_pour + objects[id].votes_contre;
            if (total_votes > 30){
              total_votes = 30;
            }
            bar_size = (180/30)*total_votes;

            switch(objects[id].vote_client)
            {
              case 0:
                disabledNon = "disabled";
                disabledOui = "";
                break;
              case 1:
                disabledOui = "disabled";
                disabledNon = "";
                break;
              default:
                disabledOui = "";
                disabledNon = "";
                break;
            }
            nonPartenaires[objects[id].id] = {
              "id": objects[id].id,
              "latitude": lat,
              "longitude": lng,
              "nom": objects[id].enseigne.nom,
              "ville": objects[id].alias || objects[id].ville,
              "logo": objects[id].enseigne.logo_web,
              "distance": objects[id].distance,
              "voter": objects[id].vote_client,
              "votes_pour": objects[id].votes_pour,
              "votes_contre": objects[id].votes_contre,
              "total_votes": total_votes,
              "bar_size": bar_size,
              "disabledNon": disabledNon,
              "disabledOui": disabledOui,
              "starred": objects[id].starred_client,
            }
            markerNon.on('click', displayPopup);
            markersNon.addLayer(markerNon);
          }
        }
      }
    });
  }*/
});