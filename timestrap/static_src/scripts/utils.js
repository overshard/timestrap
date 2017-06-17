// Append number with 0 if there is only 1 digit
function pad(num) {
    num = num.toString();
    if (num.length === 1) {
        num = '0' + num;
    }
    return num;
}


// Convert a decimal duration (0.0) to a string (0:00).
function durationToString(duration) {
    if (typeof(duration) === 'number') {
        let hours = Math.floor(duration);
        let minutes = Math.round((duration - hours) * 60);
        duration = hours + ':' + pad(minutes);
    }
    return duration;
}


// Convert a decimal duration (0.0) duration to a number (0) of seconds.
function durationToSeconds(duration) {
    if (typeof(duration) === 'number') {
        let hours = Math.floor(duration);
        let minutes = Math.round((duration - hours) * 60);
        duration = hours * 3600 + minutes * 60;
    }
    return duration;
}


// Convert a number (0) of seconds to a string (0:00).
function secondsToDurationString(duration) {
    if (typeof(duration) === 'number') {
        let hours = Math.floor(duration / 3600);
        let minutes = Math.floor(duration % 3600 / 60);
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
        for (let i = 0; i < target.elements.length; i++) {
            if (target.elements.hasOwnProperty(i)
                && typeof target.elements[i].type !== 'undefined'
                && target.elements[i].type == 'submit') {
                buttons.push(target.elements[i]);
            }
        }
    }
    else {
        buttons.push(target);
    }

    for (let i = 0; i < buttons.length; i++) {
        if (buttons.hasOwnProperty(i)) {
            let button = buttons[i];
            if (typeof button.toggleClass !== 'undefined') {
                button.toggleClass('progress-bar-striped');
                button.toggleClass('progress-bar-animated');
                button.prop('disabled', function (i, val) {
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
