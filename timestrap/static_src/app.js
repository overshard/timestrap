const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./components/app.vue');
const Clients = require('./components/clients/clients.vue');
const Tasks = require('./components/tasks/tasks.vue');
const Timesheet = require('./components/timesheet/timesheet.vue');
const Reports = require('./components/reports/reports.vue');

// quickFetch must be loaded first, as it is used by other plugins.
const quickFetch = require('./plugins/quickfetch.js');
const perms = require('./plugins/permissions.js');
const user = require('./plugins/user.js');

const store = require('./store.js').default;


// Set up event bus for app-wide communication.
// @see: https://vuejs.org/v2/guide/components.html#Non-Parent-Child-Communication
Vue.prototype.bus = new Vue();


// Set up router.
Vue.use(VueRouter);
const routes = [
    { path: '/clients/', name: 'clients', component: Clients },
    { path: '/tasks/', name: 'tasks', component: Tasks },
    { path: '/timesheet/', name: 'timesheet', component: Timesheet },
    { path: '/reports/', name: 'reports', component: Reports }
];
const router = new VueRouter({
    mode: 'history',
    hasbang: false,
    linkActiveClass: 'active',
    routes
});


// Load plugins
Vue.use(quickFetch);
Vue.use(perms);
Vue.use(user);


router.beforeEach((to, from, next) => {
    Promise.all([Vue.prototype.$user, Vue.prototype.$perms]).then(function() {
        next();
    });
});


const app = new Vue({
    router,
    store,
    el: '#app',
    render(createElement) {
        return createElement(App);
    }
});
