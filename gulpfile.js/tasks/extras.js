const gulp = require('gulp');


gulp.task('extras', function() {
    return gulp.src('node_modules/font-awesome/fonts/*')
        .pipe(gulp.dest('timestrap/static/fonts/'));
});
