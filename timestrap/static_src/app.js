const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./components/app.vue');
const Clients = require('./components/clients.vue');
const Tasks = require('./components/tasks.vue');
const Timesheet = require('./components/timesheet.vue');
const Reports = require('./components/reports.vue');


// TODO: Figure out why this isn't working...
Vue.config.devtools = false;
Vue.config.debug = false;
Vue.config.silent = true;


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


const global = {
    user: quickFetch(timestrapConfig.USER.URL).then(data => {
        global.user = data;
    }).catch(error => console.log(error)),

    perms: quickFetch(timestrapConfig.API_URLS.PERMISSIONS).then(data => {
        let perms = Object;
        for (let i = 0; i < data.length; i++) {
            perms[data[i].codename] = data[i];
        }
        global.perms = perms;
    }).catch(error => console.log(error))
};
global.install = function() {
    Object.defineProperty(Vue.prototype, 'global', {
        get() { return global; }
    });
};
Vue.use(global);


const app = new Vue({
    router,
    el: '#app',
    render(createElement) {
        return createElement(App);
    }
});
