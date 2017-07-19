// Enable sending and receiving form the django-rest-framework API.
module.exports = {
    install: function(Vue, options) {
        let user = Vue.prototype.$quickFetch(timestrapConfig.USER.URL);
        let perms = Vue.prototype.$quickFetch(timestrapConfig.API_URLS.PERMISSIONS);
        Vue.prototype.$user = Promise.all([user, perms]).then(data => {
            Vue.prototype.$user = data[0];
            Vue.prototype.$user.perms = Object;
            for (let i = 0; i < data[1].length; i++) {
                Vue.prototype.$user.perms[data[1][i].codename] = data[1][i];
            }
        }).catch(error => console.log(error));
    }
};
