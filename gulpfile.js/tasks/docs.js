var gulp = require('gulp');

var concat = require('gulp-concat');

var spawn = require('child_process').spawn;
var spawnSync = require('child_process').spawnSync;


gulp.task('docs', ['docs:build', 'docs:watch']);

gulp.task('docs:build', ['docs:github', 'docs:rtd'])


gulp.task('docs:watch', function() {
    gulp.watch(['docs/**/*.md', 'docs/**/*.rst'], ['docs-github', 'docs-rtd']);
});


gulp.task('docs:github', function() {
    var files = [
        'docs/introduction/lead.md',
        'docs/introduction/demo.md',
        'docs/introduction/quickstart.md',
        'docs/installation/manual.md',
        'docs/installation/development.md',
        'docs/introduction/further_reading.md'
    ];
    gulp.src(files)
        .pipe(concat('README.md'))
        .pipe(gulp.dest('.'));
});


gulp.task('docs:rtd', function() {
    spawnSync(
        'sphinx-build',
        [
            'docs',
            'docs/_build'
        ],
        {
            stdio: 'inherit'
        }
    );
});
