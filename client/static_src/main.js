import Vue from 'vue';

import App from './components/app.vue';

import VueMoment from './plugins/moment';
import perms from './plugins/permissions';

import router from './router';
import store from './store';


// Global event bus

Vue.prototype.bus = new Vue();


// Plugins

Vue.use(VueMoment);
Vue.use(perms);


// Promise user and permissions to all routes

router.beforeEach((to, from, next) => {
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
