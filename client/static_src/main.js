import './assets';

import Vue from 'vue';

import VueMoment from './plugins/moment';
import VuePermissions from './plugins/permissions';

import App from './components/app.vue';

import router from './router';
import store from './store';



// Global event bus

Vue.prototype.bus = new Vue();


// Sockets
// TODO: Improve sockets, move to it's own file atleast...

let updateSocketProtocol = 'ws://';
if (location.protocol == 'https:') updateSocketProtocol = 'wss://';
let updateSocketUrl = updateSocketProtocol + window.location.host + '/socket/';

let updateSocket = new WebSocket(updateSocketUrl);

updateSocket.onclose = () => {
  console.error('Update socket closed unexpectedly.');
};

updateSocket.onerror = () => {
  console.error('Update socket errored unexpectedly.');
};

updateSocket.onmessage = e => {
  let updateData = JSON.parse(e.data);
  if (updateData.tasks != store.getters['tasks/getNumberOfTasks']) store.dispatch('tasks/getTasks');
  if (updateData.clients != store.getters['clients/getNumberOfClients']) store.dispatch('clients/getClients');
  if (updateData.projects != store.getters['clients/getNumberOfProjects']) store.dispatch('clients/getProjects');
};

function checkForUpdates() {
  setTimeout(() => {
    updateSocket.send('');
    checkForUpdates();
  }, 5000);
}

checkForUpdates();


// Plugins

Vue.use(VueMoment);
Vue.use(VuePermissions);


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
