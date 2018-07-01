const gulp = require('gulp');
const concat = require('gulp-concat');

const spawn = require('child_process').spawn;


gulp.task('docs:github', () => {
  return gulp.src([
    'docs/introduction/lead.md',
    'docs/introduction/demo.md',
    'docs/introduction/quickstart.md',
    'docs/installation/docker.md',
    'docs/installation/development.md',
    'docs/introduction/further_reading.md',
  ])
    .pipe(concat('README.md'))
    .pipe(gulp.dest('.'));
});


gulp.task('docs:rtd', cb => {
  spawn(
    'pipenv',
    ['run', 'sphinx-build', 'docs', 'docs/_build'],
    {stdio: 'inherit'}
  ).on('exit', code => {
    if (code !== 0) process.exit(code);
    return cb;
  });
});
