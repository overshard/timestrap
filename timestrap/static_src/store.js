const Vue = require('vue');
const Vuex = require('vuex');


Vue.use(Vuex);


exports.default = new Vuex.Store({
    state: {
        loading: true,
        tasks: [],
    },
    mutations: {
        setLoading: (state, status) => state.loading = status,
        setTasks: (state, tasks) => state.tasks = tasks,
    },
    actions: {
        getTasks({ commit }) {
            commit('setLoading', true);
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
                commit('setTasks', data);
                commit('setLoading', false);
            }).catch(error => console.error(error));
        },
    }
});
