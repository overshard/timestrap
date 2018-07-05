import './assets';

import Vue from 'vue';

import VueMoment from './plugins/moment';
import VuePermissions from './plugins/permissions';
import VueSocket from './plugins/socket';

import App from './components/app.vue';

import router from './router';
import store from './store';



// Global event bus

Vue.prototype.bus = new Vue();


// Plugins

Vue.use(VueMoment);
Vue.use(VuePermissions);
Vue.use(VueSocket);


// Promise permissions to all routes, update document title on route

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  Promise.all([Vue.prototype.$perms]).then(function() {
    next();
  });
});


// Run all store getters to start

store.dispatch('users/getUsers');
store.dispatch('tasks/getTasks');
store.dispatch('clients/getClients');
store.dispatch('clients/getProjects');
store.dispatch('entries/getEntries');


// Start vue app

new Vue({
  router,
  store,
  el: '#app',
  render(createElement) {
    return createElement(App);
  },
});
