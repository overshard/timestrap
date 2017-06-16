const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./components/app.vue');
const Clients = require('./components/clients.vue');
const Tasks = require('./components/tasks.vue');
const Timesheet = require('./components/timesheet.vue');
const Reports = require('./components/reports.vue');
const Invoicing = require('./components/invoicing.vue');


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


// Enable sending and receiving form the django-rest-framework API.
const quickFetch = function(url, method, body) {
    let csrftoken = Cookies.get('csrftoken');
    method = (typeof method !== 'undefined') ? method : 'get';

    // Give us back a promise we can .then() on, data can be accessed via
    // .then(function(data) {console.log(data)})
    return fetch(url, {
        credentials: 'include',
        headers: new Headers({
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken
        }),
        method: method,
        body: JSON.stringify(body)
    }).then(function(response) {
        let result = null;
        switch (response.status) {
        case 200:  // HTTP_200_OK
        case 201:  // HTTP_201_CREATED
            result = response.json();
            break;
        default:
            result = response;
            break;
        }
        return result;
    });
};
quickFetch.install = function() {
    Object.defineProperty(Vue.prototype, 'quickFetch', {
        get() { return quickFetch; }
    });
};
Vue.use(quickFetch);


// Set up "global" plugin with user and permissions data.
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
