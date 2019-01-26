import Vue from 'vue';

import fetch from '../../fetch';


export default {
  namespaced: true,
  state: {
    all: [],
  },
  mutations: {
    setPermissions: (state, permissions) => state.all = permissions,
  },
  actions: {
    fetchPermissions({commit}) {
      commit('addLoading', 'permissions', {root: true});
      fetch.get(timestrapConfig.API_URLS.PERMISSIONS).then(response => {
        commit('setPermissions', response.data);
        commit('removeLoading', 'permissions', {root: true});
      }).catch(error => console.log(error));
    },
  },
};
