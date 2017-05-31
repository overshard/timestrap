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


const app = new Vue({
    router,
    el: '#app',
    render(createElement) {
        return createElement(App);
    }
});
