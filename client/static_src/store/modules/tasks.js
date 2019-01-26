import Vue from 'vue';

import fetch from '../../fetch';


export default {
  namespaced: true,
  state: {
    all: [],
  },
  getters: {
    getNumberOfTasks: state => {
      return state.all.length;
    },
    getSelectTasks: state => {
      return state.all.map(task => {
        return {id: task.url, text: task.name};
      });
    },
    getSearchTasks: state => search => {
      return state.all.filter(task => {
        return task.name.toLowerCase().includes(search);
      });
    },
    getTask: state => url => {
      const task = state.all.find(task => {
        return task.url == url;
      });
      if (typeof(task) === 'undefined') return {};
      else return task;
    },
  },
  mutations: {
    setTasks: (state, tasks) => state.all = tasks,
    addTask: (state, task) => state.all.unshift(task),
    updateTask: (state, opts) => Vue.set(state.all, opts.index, opts.task),
    removeTask: (state, index) => Vue.delete(state.all, index),
  },
  actions: {
    fetchTasks({commit}) {
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
    deleteTask({commit, state}, task) {
      const index = state.all.findIndex(item => {
        return item.id === task.id;
      });
      fetch.delete(state.all[index].url).then(() => {
        commit('removeTask', index);
      }).catch(error => console.log(error));
    },
  },
};
