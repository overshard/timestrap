const Vue = require('vue');
const VueRouter = require('vue-router');

const App = require('./app.vue');
const Timesheet = require('./timesheet.vue');
const Clients = require('./clients.vue');


Vue.use(VueRouter);


const routes = [
    { path: '/timesheet/', component: Timesheet },
    { path: '/clients/', component: Clients }
];


const router = new VueRouter({
    mode: 'history',
    hasbang: false,
    linkActiveClass: 'active',
    routes
});


const app = new Vue({
    router,
    el: '#app',
    render(createElement) {
        return createElement(App);
    }
});
