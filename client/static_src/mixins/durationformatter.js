export default {
    methods: {
        // Convert a decimal duration (0.0) to a string (0:00).
        durationToString: function(duration) {
            if (typeof(duration) === 'number') {
                let hours = Math.floor(duration);
                let minutes = Math.round((duration - hours) * 60);
                duration = hours + ':' + ('00' + minutes).slice(-2);
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
        },
        // Convert a number (0) of seconds to a string (0:00).
        secondsToString: function(duration) {
            if (typeof(duration) === 'number') {
                let hours = Math.floor(duration / 3600);
                let minutes = Math.floor(duration % 3600 / 60);
                duration = hours + ':' + ('00' + minutes).slice(-2);
            }
            return duration;
        }
    }
};
