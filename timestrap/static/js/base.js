// Promote a user to the front of a list
function promote(userId, arr) {
	let newArr = arr;

    for (let i = 0; i < newArr.length; i++) {
        if (newArr[i].id === userId) {
            let a = newArr.splice(i, 1);
            newArr.unshift(a[0]);
            break;
        }
    }

	return newArr;
}


// We use this function throughout all the things to send and recieve form our
// django-rest-framework API
function autoFetch(url, method, body) {
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
        return response.json()
    });
}
