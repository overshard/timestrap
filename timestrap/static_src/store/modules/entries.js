import Vue from 'vue';

import fetch from '../../fetch';


export default {
    namespaced: true,
    state: {
        start: moment().format('YYYY-MM-DD'),
        all: [],
        subtotal: 0,
        total: 0,
    },
    getters: {
        getSelectEntries: state => {
            return state.all.map(entry => {return {id: entry.url, text: entry.name}});
        },
        getEntriesByDay: state => {
            let allDays = [];
            for (let i = 0; i < 7; i++) {
                let day = moment(state.start).subtract(i, 'day').format('YYYY-MM-DD');
                allDays.push(day)
            }
            return allDays.map(day => {
                return {
                    date: day,
                    entries: state.all.filter(entry => {
                        return entry.date == day;
                    }),
                };
            });
        },
    },
    mutations: {
        setEntries: (state, entries) => state.all = entries,
        setTotal: (state, total) => state.total = total,
        setSubtotal: (state, subtotal) => state.subtotal = subtotal,
        addEntry: (state, entry) => state.all.unshift(entry),
        updateEntry: (state, opts) => Vue.set(state.all, opts.index, opts.entry),
        removeEntry: (state, index) => Vue.delete(state.all, index),
    },
    actions: {
        getEntries({commit, state}) {
            commit('setLoading', true, {root: true});
            fetch.get(timestrapConfig.API_URLS.ENTRIES, {params: {user: timestrapConfig.USER.ID, max_date: state.start, min_date: moment(state.start).subtract(7, 'day').format('YYYY-MM-DD')}}).then(response => {
                commit('setEntries', response.data.results);
                commit('setTotal', response.data.total_duration);
                commit('setSubtotal', response.data.subtotal_duration);
                commit('setLoading', false, {root: true});
            }).catch(error => console.log(error));
        },
        createEntry({commit}, entry) {
            fetch.post(timestrapConfig.API_URLS.ENTRIES, entry).then(response => {
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
