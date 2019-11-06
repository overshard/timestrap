import fetch from '../../fetch';


export default {
  namespaced: true,
  state: {
    all: [],
    subtotal: 0,
    total: 0,

    orderBy: null,
    orderDir: null,

    minDate: null,
    maxDate: null,
    user: null,
    client: null,
    project: null,
    task: null,
  },
  getters: {
    getSelectEntries: state => {
      return state.all.map(entry => {
        return {id: entry.url, text: entry.name};
      });
    },
  },
  mutations: {
    setEntries: (state, entries) => state.all = entries,
    setSubtotal: (state, subtotal) => state.subtotal = subtotal,
    setTotal: (state, total) => state.total = total,

    setOrderBy: (state, orderBy) => state.orderBy = orderBy,
    setOrderDir: (state, orderDir) => state.orderDir = orderDir,

    setMinDate: (state, minDate) => state.minDate = minDate,
    setMaxDate: (state, maxDate) => state.maxDate = maxDate,
    setUser: (state, user) => state.user = user,
    setClient: (state, client) => state.client = client,
    setProject: (state, project) => state.project = project,
    setTask: (state, task) => state.task = task,
  },
  actions: {
    getReport({commit, state}) {
      commit('addLoading', 'reports', {root: true});

      let ordering = (state.orderDir == 'desc' ? '-' : '') + state.orderBy;
      if (state.orderBy != 'date') ordering += ',-date';

      function urlToId(url) {
        if (url !== null) {
          let splitUrl = url.split('/');
          return splitUrl[splitUrl.length - 2];
        } else {
          return "";
        }
      }

      let getOptions = {
        params: {
          ordering: ordering,
          min_date: state.minDate,
          max_date:state.maxDate,
          user: urlToId(state.user),
          project: urlToId(state.project),
          project__client: urlToId(state.client),
          task: urlToId(state.task),
        },
      };

      fetch.get(timestrapConfig.API_URLS.ENTRIES, getOptions).then(response => {
        commit('setEntries', response.data.results);
        commit('setTotal', response.data.total_duration);
        commit('setSubtotal', response.data.subtotal_duration);
        commit('removeLoading', 'reports', {root: true});
      }).catch(error => {
        console.log(error);
        commit('setEntries', []);
        commit('setTotal', 0);
        commit('setSubtotal', 0);
        commit('removeLoading', 'reports', {root: true});
      });
    },
  },
};
