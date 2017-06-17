// Enable sending and receiving form the django-rest-framework API.
module.exports = {
    install: function(Vue, options) {
        Vue.prototype.$quickFetch = function(url, method, body) {
            let csrftoken = Cookies.get('csrftoken');
            method = (typeof method !== 'undefined') ? method : 'get';

            // Give us back a promise we can .then() on, data can be accessed via
            // .then(function(data) {console.log(data)})
            return fetch(url, {
                credentials: 'include',
                headers: new Headers({
                    'content-type': 'application/json',
                    'X-CSRFToken': csrftoken
                }),
                method: method,
                body: JSON.stringify(body)
            }).then(function(response) {
                let result = null;
                switch (response.status) {
                    case 200:  // HTTP_200_OK
                    case 201:  // HTTP_201_CREATED
                        result = response.json();
                        break;
                    default:
                        result = response;
                        break;
                }
                return result;
            });
        }
    }
};
