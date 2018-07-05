const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('manage:test', gulp.series('build:webpack:production', () => {
  let command = ['run', 'python', 'manage.py', 'test'];

  const parallel = process.argv.indexOf('--parallel');
  if (parallel !== -1) command.push(command.push('--parallel'));

  const test = process.argv.indexOf('--test');
  if (test !== -1) command.push(process.argv[test+1]);

  const head = process.argv.indexOf('--head');
  if (head !== -1) process.env.BROWSER_HEADLESS = 0;

  return spawn(
    'pipenv',
    command,
    {stdio: 'inherit', env: process.env}
  );
}));


gulp.task('manage:runserver', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'runserver'],
    {stdio: 'inherit'}
  );
});


gulp.task('manage:makemigrations', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'makemigrations'],
    {stdio: 'inherit'}
  );
});


gulp.task('manage:migrate', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'migrate'],
    {stdio: 'inherit'}
  );
});


gulp.task('manage:createsuperuser', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'createsuperuser'],
    {stdio: 'inherit'}
  );
});


gulp.task('manage:fake', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'fake'],
    {stdio: 'inherit'}
  );
});


gulp.task('manage:reset', () => {
  return spawn(
    'pipenv',
    ['run', 'python', 'manage.py', 'reset', '--no-input'],
    {stdio: 'inherit'}
  );
});
