// We use this function throughout all the things to send and recieve form our
// django-rest-framework API
function quickFetch(url, method, body) {
    let csrftoken = Cookies.get('csrftoken')
    method = (typeof method !== 'undefined') ? method : 'get'

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
        // Delete response throws an error with .json().
        // TODO: Figure out a proper way to return information on DELETE.
        if (method != 'delete') {
            return response.json()
        }
    });
}


// Append number with 0 if there is only 1 digit
function pad(num) {
    num = num.toString()
    if (num.length === 1) {
        num = '0' + num
    }
    return num
}
