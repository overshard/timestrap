module.exports = {
    install: function(Vue, options) {
        // Enable sending and receiving form the django-rest-framework API.
        Vue.prototype.$quickFetch = function(url, method, body) {
            Vue.prototype.bus.$emit('block-during-fetch', true);
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
                Vue.prototype.bus.$emit('block-during-fetch', false);
                return result;
            });
        };

        // Add a "v-block-during-fetch" directive available to components to
        // disable them while quickFetch is executing.
        Vue.directive('block-during-fetch', {
            inserted: function (el) {
                Vue.prototype.bus.$on('block-during-fetch', (block) => {
                    if (block && !el.classList.contains('fetch-blocked')) {
                        el.disabled = true;
                        el.classList.add('fetch-blocked');
                        el.classList.add('progress-bar-striped');
                        el.classList.add('progress-bar-animated');
                    }
                    else if (!block && el.classList.contains('fetch-blocked')) {
                        el.disabled = false;
                        el.classList.remove('fetch-blocked');
                        el.classList.remove('progress-bar-striped');
                        el.classList.remove('progress-bar-animated');
                    }
                });
            }
        });
    }
};
