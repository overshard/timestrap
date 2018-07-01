const gulp = require('gulp');


gulp.task('default', gulp.parallel('build:development', 'manage:runserver'));
