import Vue from 'vue';

import fetch from '../../fetch';


export default {
  namespaced: true,
  state: {
    all: [],
  },
  getters: {
    getNumberOfClients: state => {
      return state.all.length;
    },
    getSelectClients: state => {
      return state.all.map(client => {
        return {id: client.url, text: client.name};
      });
    },
    getSearchClients: state => search => {
      return state.all.filter(client => {
        return client.name.toLowerCase().includes(search);
      });
    },
    getClient: state => url => {
      const client = state.all.find(client => {
        return client.url == url;
      });
      if (typeof(client) === 'undefined') return {};
      else return client;
    },
  },
  mutations: {
    setClients: (state, clients) => state.all = clients,
    addClient: (state, client) => state.all.unshift(client),
    updateClient: (state, opts) => Vue.set(state.all, opts.index, opts.client),
    removeClient: (state, index) => Vue.delete(state.all, index),
  },
  actions: {
    fetchClients({commit}) {
      commit('addLoading', 'clients', {root: true});
      fetch.get(timestrapConfig.API_URLS.CLIENTS).then(response => {
        commit('setClients', response.data);
        commit('removeLoading', 'clients', {root: true});
      }).catch(error => console.log(error));
    },
    createClient({commit}, client) {
      fetch.post(timestrapConfig.API_URLS.CLIENTS, client).then(response => {
        commit('addClient', response.data);
      }).catch(error => console.log(error));
    },
    editClient({commit, state}, client) {
      fetch.put(client.url, client).then(response => {
        const index = state.all.findIndex(item => {
          return item.id === response.data.id;
        });
        commit('updateClient', {index: index, client: response.data});
      }).catch(error => console.log(error));
    },
    deleteClient({commit, state}, client) {
      const index = state.all.findIndex(item => {
        return item.id === client.id;
      });
      fetch.delete(state.all[index].url).then(() => {
        commit('removeClient', index);
      }).catch(error => console.log(error));
    },
  },
};
