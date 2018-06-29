const gulp = require('gulp');
const concat = require('gulp-concat');
const spawn = require('child_process').spawn;

const docsReadmeFiles = require('../../gulpfile.json').docsReadmeFiles;


gulp.task('docs', ['docs:build', 'docs:watch']);


gulp.task('docs:build', ['docs:github', 'docs:rtd']);


gulp.task('docs:watch', function() {
  gulp.watch(['docs/**/*.md', 'docs/**/*.rst'], ['docs:github', 'docs:rtd']);
});


gulp.task('docs:github', function() {
  gulp.src(docsReadmeFiles)
    .pipe(concat('README.md'))
    .pipe(gulp.dest('.'));
});


gulp.task('docs:rtd', function(cb) {
  spawn(
    'pipenv',
    [
      'run',
      'sphinx-build',
      'docs',
      'docs/_build',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', cb);
});
