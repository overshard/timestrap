const gulp = require('gulp');

const extrasFiles = require('../config.js').extrasFiles;


gulp.task('extras', function() {
    return gulp.src(extrasFiles)
        .pipe(gulp.dest('timestrap/static/fonts/'));
});
