import { Pipe, PipeTransform } from '@angular/core';
import { Poi } from './poi';

@Pipe({
  name: 'poiTags'
})
export class PoiTagsPipe implements PipeTransform {
  transform(poi: Poi): String {
    let poiTags = '';
    poi.tags.forEach(function(poiTag) {
      poiTags = poiTags + `<div class="poiContentTag">#${poiTag}</div>`;
    });
    return poiTags;
  }
}
