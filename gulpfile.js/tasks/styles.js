const gulp = require('gulp');

const concat = require('gulp-concat');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const strip = require('gulp-strip-css-comments');

const stylesFiles = require('../../gulpfile.json').stylesFiles;


gulp.task('styles', ['styles:vendor']);


gulp.task('styles:vendor', () => {
    return gulp.src(stylesFiles)
        .pipe(strip())
        .pipe(concat('bundle-vendor.css'))
        .pipe(gulp.dest('client/static/css/'));
});
