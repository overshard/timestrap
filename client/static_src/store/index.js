import Vue from 'vue';
import Vuex from 'vuex';

import entries from './modules/entries';
import tasks from './modules/tasks';
import clients from './modules/clients';
import users from './modules/users';
import reports from './modules/reports';


// Setup Vuex plugin so we can add store to our Vue

Vue.use(Vuex);


// Create and export store with all modules for use in main

export default new Vuex.Store({
  state: {
    maxLoading: 0,
    loading: [],
  },
  getters: {
    loadingPercent: (state) => {
      if (state.loading.length > 0) return (1 - (state.loading.length / state.maxLoading)) * 100;
      else return 100;
    },
    doneLoading: (state) => {
      if (state.maxLoading === 0) return true;
      else return false;
    },
  },
  mutations: {
    addLoading: (state, module) => {
      state.loading.push(module);
      state.maxLoading++;
    },
    removeLoading: (state, module) => {
      Vue.delete(
        state.loading,
        state.loading.indexOf(module),
      );
      if (state.loading.length === 0) {
        setTimeout(() => {
          state.maxLoading = 0;
        }, 500);
      }
    },
  },
  modules: {
    entries: entries,
    tasks: tasks,
    clients: clients,
    users: users,
    reports: reports,
  },
});
