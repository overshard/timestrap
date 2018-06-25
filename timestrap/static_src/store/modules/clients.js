import Vue from 'vue';


export default {
    namespaced: true,
    state: {
        allClients: [],
        allProjects: [],
    },
    getters: {
        getSelectClients: state => {
            return state.clientsAll.map(client => {return {id: client.url, text: client.name}});
        },
    },
    mutations: {
        setClients: (state, clients) => state.allClients = clients,
        addClient: (state, client) => state.allClients.unshift(client),
        updateClient: (state, opts) => Vue.set(state.allClients, opts.index, opts.client),
        removeClient: (state, index) => Vue.delete(state.allClients, index),
    },
    actions: {
        getClients({commit}) {
            commit('setLoading', true, {root: true});
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.CLIENTS).then(data => {
                commit('setClients', data);
                commit('setLoading', false, {root: true});
            }).catch(error => console.error(error));
        },
        createClient({commit}, client) {
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.CLIENTS, 'post', client).then(data => {
                commit('addClient', data);
            }).catch(error => console.log(error));
        },
        editClient({commit, state}, client) {
            Vue.prototype.$quickFetch(client.url, 'put', client).then(data => {
                const index = state.allClients.findIndex(item => {return item.id === data.id});
                commit('updateClient', {index: index, client:data});
            }).catch(error => console.log(error));
        },
        deleteClient({commit, state}, index) {
            Vue.prototype.$quickFetch(state.allClients[index].url, 'delete').then(data => {
                commit('removeClient', index);
            }).catch(error => console.log(error));
        },
    }
};
