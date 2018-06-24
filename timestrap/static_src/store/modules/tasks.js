import Vue from 'vue';


export default {
    namespaced: true,
    state: {
        all: [],
    },
    getters: {
        getSelectTasks: state => {
            return state.all.map(task => {
                return {id: task.url, text: task.name};
            });
        },
    },
    mutations: {
        setTasks: (state, tasks) => state.all = tasks,
        removeTask: (state, index) => Vue.delete(state.all, index),
    },
    actions: {
        getTasks({ commit }) {
            commit('setLoading', true, {root: true});
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
                commit('setTasks', data);
                commit('setLoading', false, {root: true});
            }).catch(error => console.error(error));
        },
        deleteTask({ commit, state }, index) {
            Vue.prototype.$quickFetch(state.all[index].url, 'delete').then(response => {
                if (response.status === 204) {
                    $.growl.notice({ message: 'Task deleted!' });
                    commit('removeTask', index);
                } else {
                    $.growl.error({ message: 'Task delete failed ):' });
                }
            });
        },
    }
};
