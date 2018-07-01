const gulp = require('gulp');


gulp.task('watch', () => {
  return gulp.watch(
    ['client/static_src/**/*.js', 'client/static_src/components/**/*.vue'],
    ['scripts']
  );
});
