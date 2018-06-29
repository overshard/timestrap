import Vue from 'vue';
import VueRouter from 'vue-router';

import Clients from './components/clients/clients.vue';
import Tasks from './components/tasks/tasks.vue';
import Timesheet from './components/timesheet/timesheet.vue';
import Reports from './components/reports/reports.vue';


Vue.use(VueRouter);


export default new VueRouter({
  mode: 'history',
  hasbang: false,
  linkActiveClass: 'active',
  routes: [
    {path: '/clients/', name: 'clients', component: Clients},
    {path: '/tasks/', name: 'tasks', component: Tasks},
    {path: '/timesheet/', name: 'timesheet', component: Timesheet},
    {path: '/reports/', name: 'reports', component: Reports},
  ],
});
