const gulp = require('gulp');

const concat = require('gulp-concat');
const sass = require('gulp-sass');
const autoprefixer = require('gulp-autoprefixer');
const strip = require('gulp-strip-css-comments');

const stylesFiles = require('../../gulpfile.json').stylesFiles;


gulp.task('styles', ['styles:vendor', 'styles:sass']);


gulp.task('styles:vendor', () => {
    return gulp.src(stylesFiles)
        .pipe(strip())
        .pipe(concat('bundle-vendor.css'))
        .pipe(gulp.dest('timestrap/static/css/'));
});


gulp.task('styles:sass', () => {
    return gulp.src('timestrap/static_src/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(concat('bundle-scss.css'))
        .pipe(gulp.dest('timestrap/static/css/'));
});
