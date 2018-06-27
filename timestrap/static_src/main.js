import Vue from 'vue';

import App from './components/app.vue';

import quickFetch from './plugins/quickfetch';
import perms from './plugins/permissions';
import user from './plugins/user';

import router from './router';
import store from './store';


// Global event bus

Vue.prototype.bus = new Vue();


// Plugins

Vue.use(quickFetch);
Vue.use(perms);
Vue.use(user);


// Promise user and permissions to all routes

router.beforeEach((to, from, next) => {
    Promise.all([Vue.prototype.$user, Vue.prototype.$perms]).then(function() {
        next();
    });
});


// Run all store getters to start

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
    }
});
