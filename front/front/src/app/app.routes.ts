import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { MainComponent } from './main/main.component';
import { CreateTrackComponent } from './create-track/create-track.component';
import { ProfileComponent } from './profile/profile.component';
import { ViewProfileComponent } from './view-profile/view-profile.component';


export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'create-track', component: CreateTrackComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'main', component: MainComponent },
  { path: 'profile/:id', component: ViewProfileComponent },
];
