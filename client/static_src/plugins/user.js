import fetch from '../fetch';


export default {
  install: Vue => {
    Vue.prototype.$user = fetch(timestrapConfig.USER.URL).then(response => {
      Vue.prototype.$user = response.data;
    }).catch(error => console.log(error));
  },
};
