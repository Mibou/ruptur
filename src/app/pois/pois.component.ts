import { Component, OnInit } from '@angular/core';
import { Poi } from '../poi';
import { Marker } from '../marker';

import * as POIDATA from '../test.json';
import * as $ from 'jquery';
import * as L from 'leaflet';

@Component({
  selector: 'app-pois',
  templateUrl: './pois.component.html',
  styleUrls: ['./pois.component.scss']
})
export class PoisComponent implements OnInit {

  private _allMarkers: Marker[] = [];
  private _map: any;
  public poidata: Poi[] = [];

  constructor() {
    this.poidata = POIDATA;
  }

  appendPoi(poi) {
    const currentMarker: Marker = L.marker(
      poi.coordinates, {
      clickable: true
    });
    currentMarker.addTo(this._map);
    this._allMarkers.push(currentMarker);
  }

  updatePois() {
    $.each(this._allMarkers, function(_, marker) { marker.remove(); });
    this.poidata.forEach(_ => this.appendPoi(_));
  }

  setView(e) {
    let poi: Poi;
    const element: any = e;
    const index = this.poidata.findIndex(poii => Number(poii.id) === Number(element.currentTarget.id));
    if (index >= 0) {
      poi = this.poidata[index];
      const Lat_Lng = new L.LatLng(poi['coordinates'][0], poi['coordinates'][1]);
      this._map.setView(Lat_Lng , 15, {pan: {animate: true, duration: 1}});
    }
  }

  prepareMap() {
    this._map = new L.Map('map').setView([46.871170, -1.013180], 9);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Tiles Courtesy of <a href="https://www.openstreetmap.org/" target="_blank">Open street map</a>' +
        '— Map data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
      minZoom: 2,
      subdomains: 'abc',
    }).addTo(this._map);
    this._map.removeControl(this._map.zoomControl);

    this._map.on('moveend', () => this.updatePois());
  }

  ngOnInit() {
    this.prepareMap();
    $(document).on('click', 'a.link-magasin', (e) => this.setView(e));
    this.updatePois();
  }

}
