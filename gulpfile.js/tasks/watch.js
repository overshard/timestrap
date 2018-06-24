const gulp = require('gulp');


gulp.task('watch', [
    'watch:app',
    'watch:components',
    'watch:plugins',
    'watch:mixins']);


gulp.task('watch:app', () => {
    return gulp.watch('timestrap/static_src/app.js', ['scripts:app']);
});


gulp.task('watch:components', () => {
    return gulp.watch('timestrap/static_src/components/**/*.vue', ['scripts:app']);
});


gulp.task('watch:plugins', () => {
    return gulp.watch('timestrap/static_src/plugins/**/*.js', ['scripts:app']);
});


gulp.task('watch:mixins', () => {
    return gulp.watch('timestrap/static_src/mixins/**/*.js', ['scripts:app']);
});
