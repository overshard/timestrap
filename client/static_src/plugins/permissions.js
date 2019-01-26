import store from '../store';


export default {
  install: Vue => {
    Vue.prototype.$perms = store.dispatch('permissions/fetchPermissions').then(() => {
      return Vue.prototype.$perms = store.getters['permissions/getPermissions'];
    });
  },
};
