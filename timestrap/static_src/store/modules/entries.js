import Vue from 'vue';

import fetch from '../../fetch';


export default {
    namespaced: true,
    state: {
        all: [],
    },
    getters: {
        getSelectEntries: state => {
            return state.all.map(entry => {return {id: entry.url, text: entry.name}});
        },
    },
    mutations: {
        setEntries: (state, entries) => state.all = entries,
        addEntry: (state, entry) => state.all.unshift(entry),
        updateEntry: (state, opts) => Vue.set(state.all, opts.index, opts.entry),
        removeEntry: (state, index) => Vue.delete(state.all, index),
    },
    actions: {
        getEntries({commit}) {
            commit('setLoading', true, {root: true});
            fetch.get(timestrapConfig.API_URLS.TASKS).then(response => {
                commit('setEntries', response.data);
                commit('setLoading', false, {root: true});
            }).catch(error => console.log(error));
        },
        createEntry({commit}, entry) {
            fetch.post(timestrapConfig.API_URLS.TASKS, entry).then(response => {
                commit('addEntry', response.data);
            }).catch(error => console.log(error));
        },
        editEntry({commit, state}, entry) {
            fetch.put(entry.url, entry).then(response => {
                const index = state.all.findIndex(item => {return item.id === response.data.id});
                commit('updateEntry', {index: index, entry: response.data});
            }).catch(error => console.log(error));

        },
        deleteEntry({commit, state}, index) {
            fetch.delete(state.all[index].url).then(response => {
                commit('removeEntry', index);
            }).catch(error => console.log(error));
        },
    }
};
