const gulp = require('gulp');


gulp.task('watch', ['watch:sass', 'watch:scripts', 'watch:app', 'watch:components']);


gulp.task('watch:sass', function() {
    return gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles:sass']);
});


gulp.task('watch:scripts', function() {
    return gulp.watch('timestrap/static_src/js/**/*.js', ['scripts:vendor']);
});


gulp.task('watch:app', function() {
    return gulp.watch('timestrap/static_src/app.js', ['scripts:app']);
});


gulp.task('watch:components', function() {
    return gulp.watch('timestrap/static_src/components/**/*.vue', ['scripts:app']);
});
