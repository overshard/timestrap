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


// Toggle disabled/enabled styles on form submit button(s).
function toggleButtonBusy(target) {
    let buttons = [];

    // The passed target may be a form object containing elements that include
    // the clicked submit button.
    if (typeof target.elements === 'object') {
        for (var i = 0; i < target.elements.length; i++) {
            if (target.elements.hasOwnProperty(i)
                && typeof target.elements[i].type !== 'undefined'
                && target.elements[i].type == 'submit') {
                buttons.push(target.elements[i]);
            }
        }
    }
    else {
        buttons.push(target)
    }

    for (var i = 0; i < buttons.length; i++) {
        if (buttons.hasOwnProperty(i)) {
            button = buttons[i];
            if (typeof button.toggleClass !== 'undefined') {
                button.toggleClass('progress-bar-striped');
                button.toggleClass('progress-bar-animated');
                button.prop("disabled", function (i, val) {
                    return !val;
                });
            }
            else {
                if (!button.disabled) {
                    button.disabled = true;
                    button.classList.add('progress-bar-striped');
                    button.classList.add('progress-bar-animated');
                }
                else {
                    button.disabled = false;
                    button.classList.remove('progress-bar-striped');
                    button.classList.remove('progress-bar-animated');
                }
            }
        }
    }
}
