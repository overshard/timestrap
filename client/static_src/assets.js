import Vue from 'vue';


// Favicon

import './imgs/favicon.ico';


// Bootstrap

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


// Font Awesome

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  faAddressBook,
  faTasks,
  faBook,
  faUserCircle,
  faList,
  faPercent,
  faEllipsisV,
  faPlus,
  faSync,
  faBriefcase,
  faComment,
  faHourglassStart,
  faHourglassEnd,
  faCalendar,
  faArrowLeft,
  faArrowRight,
  faDownload,
  faPlay,
  faStop,
} from '@fortawesome/free-solid-svg-icons';
import {
  faClock,
} from '@fortawesome/free-regular-svg-icons';
import {
  faGithub,
} from '@fortawesome/free-brands-svg-icons';

library.add(
  faAddressBook,
  faTasks,
  faBook,
  faUserCircle,
  faList,
  faPercent,
  faEllipsisV,
  faPlus,
  faSync,
  faBriefcase,
  faComment,
  faHourglassStart,
  faHourglassEnd,
  faCalendar,
  faArrowLeft,
  faArrowRight,
  faDownload,
  faPlay,
  faStop,

  faClock,

  faGithub,
);

Vue.component('icon', FontAwesomeIcon);
