// We use this function throughout all the things to send and recieve form our
// django-rest-framework API
function quickFetch(url, method, body) {
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


// Append number with 0 if there is only 1 digit
function pad(num) {
    num = num.toString();
    if (num.length === 1) {
        num = '0' + num;
    }
    return num;
}


// Convert a decimal duration to a string (0:00).
function durationToString(duration) {
    if (typeof(duration) === 'number') {
        let hours = Math.floor(duration);
        let minutes = Math.round((duration - hours) * 60);
        duration = hours + ':' + pad(minutes);
    }
    return duration;
}
