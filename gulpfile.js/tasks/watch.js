const gulp = require('gulp');


gulp.task('watch', [
    'watch:app',
    'watch:components',
]);


gulp.task('watch:app', () => {
    return gulp.watch('timestrap/static_src/**/*.js', ['scripts:app']);
});


gulp.task('watch:components', () => {
    return gulp.watch('timestrap/static_src/components/**/*.vue', ['scripts:app']);
});
