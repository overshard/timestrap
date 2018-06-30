import Vue from 'vue';

import fetch from '../../fetch';


export default {
  namespaced: true,
  state: {
    // Clients
    allClients: [],

    // Projects
    allProjects: [],
  },
  getters: {
    // Clients
    getSelectClients: state => {
      return state.allClients.map(client => {
        return {id: client.url, text: client.name};
      });
    },

    // Projects
    getSelectProjects: state => {
      return state.allClients.map(client => {
        // TODO: Should use getClientProjects getter instead to reduce code
        const projects = state.allProjects.filter(project => {
          return project.client == client.url;
        });
        return {
          text: client.name,
          children: projects.map(project => {
            return {
              id: project.url,
              text: project.name,
            };
          }),
        };
      });
    },

    // Clients & Projects
    getClientProjects: state => clientUrl => {
      return state.allProjects.filter(project => {
        return project.client == clientUrl;
      });
    },
  },
  mutations: {
    // Clients
    setClients: (state, clients) => state.allClients = clients,
    addClient: (state, client) => state.allClients.unshift(client),
    updateClient: (state, opts) => Vue.set(state.allClients, opts.index, opts.client),
    removeClient: (state, index) => Vue.delete(state.allClients, index),

    // Projects
    setProjects: (state, projects) => state.allProjects = projects,
    addProject: (state, project) => state.allProjects.unshift(project),
    updateProject: (state, opts) => Vue.set(state.allProjects, opts.index, opts.project),
    removeProject: (state, index) => Vue.delete(state.allProjects, index),
  },
  actions: {
    // Clients
    getClients({commit}) {
      commit('setLoading', true, {root: true});
      fetch.get(timestrapConfig.API_URLS.CLIENTS).then(response => {
        commit('setClients', response.data);
        commit('setLoading', false, {root: true});
      }).catch(error => console.log(error));
    },
    createClient({commit}, client) {
      fetch.post(timestrapConfig.API_URLS.CLIENTS, client).then(response => {
        commit('addClient', response.data);
      }).catch(error => console.log(error));
    },
    editClient({commit, state}, client) {
      fetch.put(client.url, client).then(response => {
        const index = state.allClients.findIndex(item => {
          return item.id === response.data.id;
        });
        commit('updateClient', {index: index, client: response.data});
      }).catch(error => console.log(error));
    },
    deleteClient({commit, state}, index) {
      fetch.delete(state.allClients[index].url).then(() => {
        commit('removeClient', index);
      }).catch(error => console.log(error));
    },
    archiveClient({commit, state}, index) {
      let client = state.allClients[index];
      client.archive = true;
      fetch.put(client.url, client).then(() => {
        commit('removeClient', index);
      }).catch(error => console.log(error));
    },

    // Projects
    getProjects({commit}) {
      commit('setLoading', true, {root: true});
      fetch.get(timestrapConfig.API_URLS.PROJECTS).then(response => {
        commit('setProjects', response.data);
        commit('setLoading', false, {root: true});
      }).catch(error => console.log(error));
    },
    createProject({commit}, project) {
      fetch.post(timestrapConfig.API_URLS.PROJECTS, project).then(response => {
        commit('addProject', response.data);
      }).catch(error => console.log(error));
    },
    editProject({commit, state}, project) {
      fetch.put(project.url, project).then(response => {
        const index = state.allProjects.findIndex(item => {
          return item.id === response.data.id;
        });
        commit('updateProject', {index: index, project: response.data});
      }).catch(error => console.log(error));
    },
    deleteProject({commit, state}, index) {
      fetch.delete(state.allProjects[index].url).then(() => {
        commit('removeProject', index);
      }).catch(error => console.log(error));
    },
    archiveProject({commit, state}, index) {
      let project = state.allProjects[index];
      project.archive = true;
      fetch.put(project.url, project).then(() => {
        commit('removeProject', index);
      }).catch(error => console.log(error));
    },
  },
};
