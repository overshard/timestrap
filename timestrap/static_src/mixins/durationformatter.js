module.exports = {
    methods: {
        // Convert a decimal duration (0.0) to a string (0:00).
        durationToString: function(duration) {
            if (typeof(duration) === 'number') {
                let hours = Math.floor(duration);
                let minutes = Math.round((duration - hours) * 60);
                duration = hours + ':' + pad(minutes);
            }
            return duration;
        },
        // Convert a decimal duration (0.0) duration to a number (0) of seconds.
        durationToSeconds: function(duration) {
            if (typeof(duration) === 'number') {
                let hours = Math.floor(duration);
                let minutes = Math.round((duration - hours) * 60);
                duration = hours * 3600 + minutes * 60;
            }
            return duration;
        }
    }
};
