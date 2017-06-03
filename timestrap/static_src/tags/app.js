const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./app.vue');
const Clients = require('./clients.vue');
const Tasks = require('./tasks.vue');
const Timesheet = require('./timesheet.vue');


Vue.use(VueRouter);


const routes = [
    { path: '/clients/', component: Clients },
    { path: '/tasks/', component: Tasks },
    { path: '/timesheet/', component: Timesheet }
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
