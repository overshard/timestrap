// Enable sending and receiving form the django-rest-framework API.
module.exports = {
    install: function(Vue, options) {
        Vue.prototype.$perms = {};
        Vue.prototype.$quickFetch(timestrapConfig.API_URLS.PERMISSIONS).then(data => {
            let perms = Object;
            for (let i = 0; i < data.length; i++) {
                perms[data[i].codename] = data[i];
            }
            Vue.prototype.$perms = perms;
        }).catch(error => console.log(error))
    }
};
