const gulp = require('gulp');


gulp.task('default', gulp.parallel('build', 'manage:runserver'));
