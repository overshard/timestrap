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
  faPercentage,
  faEllipsisV,
  faEllipsisH,
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
  faCodeBranch,
  faClock,
  faHandHoldingUsd,
  faCaretDown,
  faCaretUp,
} from '@fortawesome/free-solid-svg-icons';

library.add(
  faAddressBook,
  faTasks,
  faBook,
  faUserCircle,
  faList,
  faPercentage,
  faEllipsisV,
  faEllipsisH,
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
  faCodeBranch,
  faClock,
  faHandHoldingUsd,
  faCaretDown,
  faCaretUp,
);

Vue.component('icon', FontAwesomeIcon);
