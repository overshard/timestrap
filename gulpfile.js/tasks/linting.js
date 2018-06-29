const gulp = require('gulp');

const eslint = require('gulp-eslint');
const sasslint = require('gulp-sass-lint');

const spawn  = require('child_process').spawn;


gulp.task('lint', ['lint:python', 'lint:sass', 'lint:es']);


gulp.task('lint:python', function(cb) {
    spawn(
        'pipenv',
        [
            'run',
            'flake8',
            '--exclude=node_modules,migrations'
        ],
        {
            stdio: 'inherit'
        }
    ).on('exit', cb);
});


gulp.task('lint:sass', function() {
    // return gulp.src('client/static_src/components/**/*.vue')
    //     .pipe(sasslint({
    //         rules: {
    //             'no-vendor-prefixes': 2,
    //             'no-ids': 0,
    //             'indentation': [1, {'size': 4}],
    //             'property-sort-order': 0,
    //             'force-element-nesting': 0,
    //         },
    //     }))
    //     .pipe(sasslint.format())
    //     .pipe(sasslint.failOnError());
});


gulp.task('lint:es', function() {
    return gulp.src([
        'gulpfile.js/**/*.js',
        'client/static_src/**/*.js',
        'client/static_src/components/**/*.vue'])
        .pipe(eslint())
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});
