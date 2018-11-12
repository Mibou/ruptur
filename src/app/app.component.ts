import { Component, AfterViewInit } from '@angular/core';
import * as poidata from './test.json';
import * as $ from 'jquery';

declare let L;

interface Marker {
  addTo(map: any);
  remove();
}

interface Poi {
  id: Number;
  type: String;
  title: String;
  subtitle: String;
  tags: String[];
  coordinates: Number[];
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements AfterViewInit {
  title = 'Association Ruptur - Accueil - Devenez acteurs de la blue economy !';

  ngAfterViewInit() {
    const allMarkers: Marker[] = [];
    let pois: Poi[] = [];
    const map = L.map('map').setView([46.871170, -1.013180], 9);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Tiles Courtesy of <a href="https://www.openstreetmap.org/" target="_blank">Open street map</a>' +
        '— Map data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
      minZoom: 2,
      reuseTiles: true,
      subdomains: 'abc',
    }).addTo(map);
    map.removeControl(map.zoomControl);

    function updatePois() {
      $.each(allMarkers, function(index, marker) { marker.remove(); });

      $('#filter').html('');
      poidata.forEach(function(poi) {
        $('#filter').append(generateInfoDiv(poi));
        const currentMarker: Marker = L.marker(
          poi.coordinates, {
          clickable: true
        });
        currentMarker.addTo(map);
        allMarkers.push(currentMarker);
      });

    }

    function generateInfoDiv(poi) {
      let poiTags = '';
      poi.tags.forEach(function(poiTag) {
        poiTags = poiTags + `<div class="poiContentTag">#${poiTag}</div>`;
      });
      // tslint:disable-next-line:max-line-length
      return `<a id="${poi.id}" class="link-magasin" title="${poi.title}"><div class="poiListItem"><div class="poiIconWrapper"><div class="poiIcon"><i class="poiIcon fa fa-${poi.type}"></i></div></div><div class="poiContent"><div class="poiContentTitle">${poi.title}</div><div class="poiContentSubtitle">${poi.subtitle}</div><div class="poiContentTags">${poiTags}</div></div></div></a>`;
    }

    $(document).on('click', '.link-magasin', function() {
      let poi: Poi;
      const element: any = this;
      const index = poidata.findIndex(poii => Number(poii.id) === Number(element.id));
      poi = poidata[index];
      const Lat_Lng = new L.LatLng(poi['coordinates'][0], poi['coordinates'][1]);
      map.setView(Lat_Lng , 15, {pan: {animate: true, duration: 1}});
    });

    updatePois();

    map.on('moveend', function (e) {
      updatePois();
    });
  }
}
