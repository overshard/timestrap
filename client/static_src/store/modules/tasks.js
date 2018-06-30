import Vue from 'vue';

import fetch from '../../fetch';


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
    addTask: (state, task) => state.all.unshift(task),
    updateTask: (state, opts) => Vue.set(state.all, opts.index, opts.task),
    removeTask: (state, index) => Vue.delete(state.all, index),
  },
  actions: {
    getTasks({commit}) {
      commit('addLoading', 'tasks', {root: true});
      fetch.get(timestrapConfig.API_URLS.TASKS).then(response => {
        commit('setTasks', response.data);
        commit('removeLoading', 'tasks', {root: true});
      }).catch(error => console.log(error));
    },
    createTask({commit}, task) {
      fetch.post(timestrapConfig.API_URLS.TASKS, task).then(response => {
        commit('addTask', response.data);
      }).catch(error => console.log(error));
    },
    editTask({commit, state}, task) {
      fetch.put(task.url, task).then(response => {
        const index = state.all.findIndex(item => {
          return item.id === response.data.id;
        });
        commit('updateTask', {index: index, task: response.data});
      }).catch(error => console.log(error));
    },
    deleteTask({commit, state}, index) {
      fetch.delete(state.all[index].url).then(() => {
        commit('removeTask', index);
      }).catch(error => console.log(error));
    },
  },
};
