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
    {path: '/clients/', name: 'clients', component: Clients, meta: {title: 'Clients — ' + timestrapConfig.SITE.NAME}},
    {path: '/tasks/', name: 'tasks', component: Tasks, meta: {title: 'Tasks — ' + timestrapConfig.SITE.NAME}},
    {path: '/timesheet/', name: 'timesheet', component: Timesheet, meta: {title: 'Timesheet — ' + timestrapConfig.SITE.NAME}},
    {path: '/reports/', name: 'reports', component: Reports, meta: {title: 'Reports — ' + timestrapConfig.SITE.NAME}},
  ],
});
