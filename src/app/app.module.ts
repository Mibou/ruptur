import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PoisComponent } from './pois/pois.component';
import { PoiTagsPipe } from './poi-tags.pipe';

@NgModule({
  declarations: [
    AppComponent,
    PoisComponent,
    PoiTagsPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
