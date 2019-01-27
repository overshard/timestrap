import Vue from 'vue';


// Images

import './imgs/favicon.ico';
import './imgs/background.jpg';


// Bootstrap

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


// Font Awesome

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {fas} from '@fortawesome/free-solid-svg-icons';
import {library} from '@fortawesome/fontawesome-svg-core';

library.add(fas);
Vue.component('icon', FontAwesomeIcon);
