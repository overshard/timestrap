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
  getters: {
    getPermissions: state => {
      return state.all.reduce((object, permission) => {
        object[permission.codename] = permission;
        return object;
      });
    },
  },
  actions: {
    fetchPermissions({commit}) {
      return new Promise((resolve, reject) => {
        commit('addLoading', 'permissions', {root: true});
        fetch.get(timestrapConfig.API_URLS.PERMISSIONS).then(response => {
          commit('setPermissions', response.data);
          commit('removeLoading', 'permissions', {root: true});
          resolve();
        }).catch(error => {
          console.log(error);
          reject();
        });
      });
    },
  },
};
