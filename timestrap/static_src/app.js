const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./components/app.vue');
const Clients = require('./components/clients.vue');
const Tasks = require('./components/tasks.vue');
const Timesheet = require('./components/timesheet.vue');
const Reports = require('./components/reports.vue');
const Invoicing = require('./components/invoicing.vue');

// quickFetch must be loaded first, as it is used by other plugins.
const quickFetch = require('./plugins/quickfetch.js');
const user = require('./plugins/user.js');
const perms = require('./plugins/permissions.js');

// TODO: Figure out why this isn't working...
Vue.config.devtools = false;
Vue.config.debug = false;
Vue.config.silent = true;


// Set up router.
Vue.use(VueRouter);
const routes = [
    { path: '/clients/', name: 'clients', component: Clients },
    { path: '/tasks/', name: 'tasks', component: Tasks },
    { path: '/timesheet/', name: 'timesheet', component: Timesheet },
    { path: '/reports/', name: 'reports', component: Reports },
    { path: '/invoicing/', name: 'invoicing', component: Invoicing }
];
const router = new VueRouter({
    mode: 'history',
    hasbang: false,
    linkActiveClass: 'active',
    routes
});


// Load plugins
Vue.use(quickFetch);
Vue.use(user);
Vue.use(perms);


// Set up event bus for app-wide communication.
// @see: https://vuejs.org/v2/guide/components.html#Non-Parent-Child-Communication
Vue.prototype.bus = new Vue();


const app = new Vue({
    router,
    el: '#app',
    render(createElement) {
        return createElement(App);
    }
});
