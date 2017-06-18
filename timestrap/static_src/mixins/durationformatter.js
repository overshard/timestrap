module.exports = {
    methods: {
        // Convert a decimal duration (0.0) to a string (0:00).
        durationToString: function (duration) {
            if (typeof(duration) === 'number') {
                let hours = Math.floor(duration);
                let minutes = Math.round((duration - hours) * 60);
                duration = hours + ':' + pad(minutes);
            }
            return duration;
        }
    }
};
