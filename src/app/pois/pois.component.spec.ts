import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import {} from 'jasmine';
import { PoisComponent } from './pois.component';
import { PoiTagsPipe } from '../poi-tags.pipe';

describe('PoisComponent', () => {
  let component: PoisComponent;
  let fixture: ComponentFixture<PoisComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PoisComponent, PoiTagsPipe ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PoisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
