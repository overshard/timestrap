// Retrieve Django User object data.
module.exports = {
    install: function(Vue, options) {
        Vue.prototype.$user = Vue.prototype.$quickFetch(timestrapConfig.USER.URL).then(data => {
            Vue.prototype.$user = data;
        }).catch(error => console.log(error));
    }
};