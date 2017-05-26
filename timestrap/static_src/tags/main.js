var Vue = require('vue')
var App = require('./app.vue')

new Vue({
    el: '#app',
    render: function (createElement) {
        return createElement(App)
    },
    use: {
        VueRouter
    }
});
