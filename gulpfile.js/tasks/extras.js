var gulp         = require('gulp');


gulp.task('extras', function() {
    var files = [
        'node_modules/font-awesome/fonts/*'
    ];
    gulp.src(files)
        .pipe(gulp.dest('timestrap/static/fonts/'));
});
