const gulp = require('gulp');

const extrasFiles = require('../../gulpfile.json').extrasFiles;


gulp.task('extras', function() {
    return gulp.src(extrasFiles)
        .pipe(gulp.dest('client/static/fonts/'));
});
