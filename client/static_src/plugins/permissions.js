import fetch from '../fetch';


export default {
  install: Vue => {
    Vue.prototype.$perms = fetch(timestrapConfig.API_URLS.PERMISSIONS).then(response => {
      let perms = Object;
      for (let i = 0; i < response.data.length; i++) {
        perms[response.data[i].codename] = response.data[i];
      }
      Vue.prototype.$perms = perms;
    }).catch(error => console.error(error));
  },
};
