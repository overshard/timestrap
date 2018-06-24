import Vue from 'vue';


export default {
    namespaced: true,
    state: {
        all: [],
    },
    getters: {
        getSelectTasks: state => {
            return state.all.map(task => {return {id: task.url, text: task.name}});
        },
    },
    mutations: {
        setTasks: (state, tasks) => state.all = tasks,
        addTask: (state, task) => state.all.unshift(task),
        updateTask: (state, opts) => Vue.set(state.all, opts.index, opts.task),
        removeTask: (state, index) => Vue.delete(state.all, index),
    },
    actions: {
        getTasks({commit}) {
            commit('setLoading', true, {root: true});
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.TASKS).then(data => {
                commit('setTasks', data);
                commit('setLoading', false, {root: true});
            }).catch(error => console.error(error));
        },
        createTask({commit}, task) {
            Vue.prototype.$quickFetch(timestrapConfig.API_URLS.TASKS, 'post', task).then(data => {
                commit('addTask', data);
            }).catch(error => console.log(error));
        },
        editTask({commit, state}, task) {
            Vue.prototype.$quickFetch(task.url, 'put', task).then(data => {
                const index = state.all.findIndex(item => {return item.id === data.id});
                commit('updateTask', {index: index, task:data});
            }).catch(error => console.log(error));
        },
        deleteTask({commit, state}, index) {
            Vue.prototype.$quickFetch(state.all[index].url, 'delete').then(data => {
                commit('removeTask', index);
            }).catch(error => console.log(error));
        },
    }
};
