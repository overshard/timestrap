var gulp         = require('gulp');


gulp.task('watch', function() {
    gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles']);
    gulp.watch('timestrap/static_src/scripts/**/*.js', ['scripts']);
    gulp.watch('timestrap/static_src/tags/**/*.tag', ['tags']);
});
