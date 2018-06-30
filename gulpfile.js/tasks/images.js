const gulp = require('gulp');

const imagesFiles = require('../../gulpfile.json').imagesFiles;


gulp.task('images', function() {
  return gulp.src(imagesFiles)
    .pipe(gulp.dest('client/static/imgs/'));
});
