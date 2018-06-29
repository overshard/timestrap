import Vue from 'vue';
import Vuex from 'vuex';

import entries from './modules/entries';
import tasks from './modules/tasks';
import clients from './modules/clients';
import users from './modules/users';


// Setup Vuex plugin so we can add store to our Vue

Vue.use(Vuex);


// Create and export store with all modules for use in main

export default new Vuex.Store({
  state: {
    loading: true,
  },
  mutations: {
    setLoading: (state, status) => state.loading = status,
  },
  modules: {
    entries: entries,
    tasks: tasks,
    clients: clients,
    users: users,
  },
});
