import './assets';

import Vue from 'vue';

import VueMoment from './plugins/moment';
import VueSocket from './plugins/socket';
import VuePermissions from './plugins/permissions';

import App from './components/app.vue';

import router from './router';
import store from './store';



// Global event bus

Vue.prototype.$bus = new Vue();


// Plugins

Vue.use(VueMoment);
Vue.use(VueSocket);
Vue.use(VuePermissions);


// Promise permissions to all routes, update document title on route

router.beforeEach((to, from, next) => {
  Promise.all([Vue.prototype.$perms]).then(function() {
    next();
  });
  document.title = to.meta.title;
});


// Run all store getters to start

store.dispatch('users/fetchUsers');
store.dispatch('tasks/fetchTasks');
store.dispatch('clients/fetchClients');
store.dispatch('projects/fetchProjects');
store.dispatch('entries/fetchEntries');


// Start vue app

new Vue({
  router,
  store,
  el: '#app',
  render(createElement) {
    return createElement(App);
  },
});
