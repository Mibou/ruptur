import { PoiTagsPipe } from './poi-tags.pipe';
import { Poi } from './poi';

describe('PoiTagsPipe', () => {
  it('create an instance', () => {
    const pipe = new PoiTagsPipe();
    expect(pipe).toBeTruthy();
  });
  it('providing poi returns poitags', () => {
    const poi: Poi = {
      id: 1,
      type: 'user',
      title: 'Alain DURET',
      subtitle: 'Immobilier',
      tags: ['Recyclage déchets', 'Energies renouvelables'],
      coordinates: [46.8711, -1.0131]
    };

    const pipe = new PoiTagsPipe();
    expect(pipe.transform(poi)).toBe(
      '<div class="poiContentTag">#Recyclage déchets</div><div class="poiContentTag">#Energies renouvelables</div>'
    );
  });
});
