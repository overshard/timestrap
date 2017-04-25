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
        return response.json()
    });
}


// Append number with 0 if there is only 1 digit
function pad(num) {
    num = num.toString();
    if (num.length === 1) {
        num = '0' + num;
    }
    return num
}


// Convert time string to seconds
function getTimeInSeconds(time) {
    let timeInSeconds = 0;
    time = time.split(':');
    timeInSeconds += parseInt(time[0])*3600;
    timeInSeconds += parseInt(time[1])*60;
    timeInSeconds += parseInt(time[2]);
    return timeInSeconds;
}


// Takes entries and outputs string
function getTotalTime(entries) {
    let totalSeconds = 0;
    for (var entry in entries) {
        totalSeconds += getTimeInSeconds(entries[entry].duration);
    }
    let hours = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600;
    let minutes = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;
    return hours +':'+ ('0'+minutes).slice(-2) +':'+ ('0'+seconds).slice(-2);
}
