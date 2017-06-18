const gulp = require('gulp');


gulp.task('watch', [
    'watch:sass',
    'watch:app',
    'watch:components',
    'watch:plugins',
    'watch:mixins']);


gulp.task('watch:sass', function() {
    return gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles:sass']);
});


gulp.task('watch:app', function() {
    return gulp.watch('timestrap/static_src/app.js', ['scripts:app']);
});


gulp.task('watch:components', function() {
    return gulp.watch('timestrap/static_src/components/**/*.vue', ['scripts:app']);
});

gulp.task('watch:plugins', function() {
    return gulp.watch('timestrap/static_src/plugins/**/*.js', ['scripts:app']);
});

gulp.task('watch:mixins', function() {
    return gulp.watch('timestrap/static_src/mixins/**/*.js', ['scripts:app']);
});
