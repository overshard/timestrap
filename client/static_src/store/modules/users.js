import Vue from 'vue';

import fetch from '../../fetch';


export default {
    namespaced: true,
    state: {
        all: [],
    },
    getters: {
        getSelectUsers: state => {
            return state.all.map(user => {
                return {id: user.url, text: user.username};
            });
        },
    },
    mutations: {
        setUsers: (state, users) => state.all = users,
        addUser: (state, user) => state.all.unshift(user),
        updateUser: (state, opts) => Vue.set(state.all, opts.index, opts.user),
        removeUser: (state, index) => Vue.delete(state.all, index),
    },
    actions: {
        getUsers({commit}) {
            commit('setLoading', true, {root: true});
            fetch.get(timestrapConfig.API_URLS.USERS).then(response => {
                commit('setUsers', response.data);
                commit('setLoading', false, {root: true});
            }).catch(error => console.log(error));
        },
        createUser({commit}, user) {
            fetch.post(timestrapConfig.API_URLS.USERS, user).then(response => {
                commit('addUser', response.data);
            }).catch(error => console.log(error));
        },
        editUser({commit, state}, user) {
            fetch.put(user.url, user).then(response => {
                const index = state.all.findIndex(item => {
                    return item.id === response.data.id;
                });
                commit('updateUser', {index: index, user: response.data});
            }).catch(error => console.log(error));
        },
        deleteUser({commit, state}, index) {
            fetch.delete(state.all[index].url).then(() => {
                commit('removeUser', index);
            }).catch(error => console.log(error));
        },
    },
};
