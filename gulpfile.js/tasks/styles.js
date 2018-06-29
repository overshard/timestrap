const gulp = require('gulp');

const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');

const stylesFiles = require('../../gulpfile.json').stylesFiles;


gulp.task('styles', ['styles:vendor']);


gulp.task('styles:vendor', () => {
    return gulp.src(stylesFiles)
        .pipe(cleanCSS({
            level: {1: {specialComments: 0}},
            rebase: false
        }))
        .pipe(concat('bundle-vendor.css'))
        .pipe(gulp.dest('client/static/css/'));
});
