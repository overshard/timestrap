var gulp         = require('gulp');


gulp.task('watch', ['watch:styles', 'watch:scripts', 'watch:tags']);


gulp.task('watch:styles', function() {
    return gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles']);
});


gulp.task('watch:scripts', function() {
    return gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles']);
});


gulp.task('watch:tags', function() {
    return gulp.watch('timestrap/static_src/tags/**/*.tag', ['tags']);
});
