// Append number with 0 if there is only 1 digit
function pad(num) {
    num = num.toString();
    if (num.length === 1) {
        num = '0' + num;
    }
    return num;
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
