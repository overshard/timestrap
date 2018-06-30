const gulp = require('gulp');

const spawn = require('child_process').spawn;


gulp.task('test', (cb) => {
  const command = ['run', 'python', 'manage.py', 'test'];
  const args = process.argv;
  const env = process.env;

  const test = args.indexOf('--test');
  if (test !== -1) command.push(args[test+1]);

  const head = args.indexOf('--head');
  if (head !== -1) env.FIREFOX_HEADLESS = 0;

  spawn('pipenv', command, {stdio: 'inherit', env: env})
    .on('exit', (code) => {
      process.exit(code);
    })
    .on('exit', cb);
});


gulp.task('coverage', (cb) => {
  spawn(
    'pipenv',
    [
      'run',
      'coverage',
      'run',
      '--source=conf,core,api',
      'manage.py',
      'test',
    ],
    {
      stdio: 'inherit',
    }
  ).on('exit', (code) => {
    if (code != 0) process.exit(code);
    spawn(
      'pipenv',
      [
        'run',
        'coverage',
        'report',
        '-m',
      ],
      {
        stdio: 'inherit',
      }
    ).on('exit', (code) => {
      if (code != 0) process.exit(code);
      return cb;
    });
  });
});
