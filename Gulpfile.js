var gulp       = require('gulp');

var expect       = require('gulp-expect-file');
var concat       = require('gulp-concat');
var sass         = require('gulp-sass');
var sasslint     = require('gulp-sass-lint');
var autoprefixer = require('gulp-autoprefixer');
var riot         = require('gulp-riot');
var eslint       = require('gulp-eslint');

var spawn      = require('child_process').spawn;
var spawnSync  = require('child_process').spawnSync;


// Primary tasks for dealing with static files
gulp.task('styles', function() {
    var files = [
        'node_modules/font-awesome/css/font-awesome.min.css',
        'node_modules/tether/dist/css/tether.min.css',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/select2/dist/css/select2.min.css',
        'node_modules/pickadate/lib/compressed/themes/default.css',
        'node_modules/pickadate/lib/compressed/themes/default.date.css',
        'static_src/sass/**/*.scss'
    ];
    gulp.src(files)
        .pipe(expect(files))
        .pipe(sass().on('error', sass.logError))
        .pipe(concat('styles.css'))
        .pipe(gulp.dest('./timestrap/static/css/'));
});


gulp.task('scripts', function(){
    var files = [
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/moment/min/moment.min.js',
        'node_modules/tether/dist/js/tether.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/select2/dist/js/select2.min.js',
        'node_modules/pickadate/lib/compressed/picker.js',
        'node_modules/pickadate/lib/compressed/picker.date.js',
        'node_modules/js-cookie/src/js.cookie.js',
        'node_modules/chart.js/dist/Chart.min.js',
        'node_modules/riot/riot+compiler.min.js',
        'node_modules/riot-route/dist/route.min.js',
        'static_src/scripts/**/*.js'
    ];
    gulp.src(files)
        .pipe(expect(files))
        .pipe(concat('scripts.js'))
        .pipe(gulp.dest('./timestrap/static/js/'));
});


gulp.task('tags', function() {
    var files = [
        'static_src/tags/**/*.tag'
    ];
    gulp.src(files)
        .pipe(expect(files))
        .pipe(riot())
        .pipe(concat('tags.js'))
        .pipe(gulp.dest('./timestrap/static/js/'));
});


gulp.task('extras', function() {
    var files = [
        'node_modules/font-awesome/fonts/*'
    ];
    gulp.src(files)
        .pipe(expect(files))
        .pipe(gulp.dest('./timestrap/static/fonts/'));
});


gulp.task('build', ['styles', 'scripts', 'tags', 'extras']);


gulp.task('watch', function() {
    gulp.watch('static_src/sass/**/*.scss', ['styles']);
    gulp.watch('static_src/scripts/**/*.js', ['scripts']);
    gulp.watch('static_src/tags/**/*.tag', ['tags']);
});


// Default to watching for static file changes and running django
gulp.task('default', ['build', 'watch'], function() {
    spawn(
        'python',
        [
            'manage.py',
            'runserver'
        ],
        {
            stdio: 'inherit'
        }
    );
});


// Linting
gulp.task('pythonlint', function() {
    var pg_dump = spawnSync(
        'flake8',
        [
            '--exclude=venv,node_modules,migrations'
        ],
        {
            stdio: 'inherit'
        }
    );
});


gulp.task('sasslint', function() {
    gulp.src('static_src/sass/**/*.s+(a|c)ss')
        .pipe(sasslint({
            rules: {
                'no-vendor-prefixes': 2,
                'no-ids': 0,
                'indentation': [
                    1,
                    {
                        'size': 4
                    }
                ],
                'property-sort-order': 0,
                'force-element-nesting': 0
            }
        }))
        .pipe(sasslint.format())
        .pipe(sasslint.failOnError());
});


gulp.task('eslint', function() {
    var files = [
        'Gulpfile.js',
        'static_src/scripts/**/*.js',
        'static_src/tags/**/*.tag'
    ];
    gulp.src(files)
        .pipe(expect(files))
        .pipe(eslint({
            'rules': {
                'indent': [
                    'error',
                    4
                ],
                'linebreak-style': [
                    'error',
                    'unix'
                ],
                'quotes': [
                    'error',
                    'single'
                ],
                'semi': [
                    'error',
                    'always'
                ]
            },
            'globals': [
                '$',
                'riot'
            ],
            'env': {
                'browser': true
            },
            'extends': 'eslint:recommended',
            'plugins': [
                'riot'
            ],
            'parserOptions': {
                'ecmaVersion': 6
            }
        }))
        .pipe(eslint.format())
        .pipe(eslint.failAfterError());
});


gulp.task('lint', ['pythonlint', 'sasslint', 'eslint']);


// Database management tasks
gulp.task('makemigrations', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'makemigrations'
        ],
        {
            stdio: 'inherit'
        }
    );
});


gulp.task('migrate', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'migrate'
        ],
        {
            stdio: 'inherit'
        }
    );
});


gulp.task('createsuperuser', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'createsuperuser'
        ],
        {
            stdio: 'inherit'
        }
    );
});


gulp.task('reset', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'flush',
            '--noinput'
        ],
        {
            stdio: 'inherit'
        }
    );
    spawnSync(
        'python',
        [
            'manage.py',
            'heroku'
        ],
        {
            stdio: 'inherit'
        }
    );
    spawnSync(
        'python',
        [
            'manage.py',
            'fake'
        ],
        {
            stdio: 'inherit'
        }
    );
});

// Testing tasks
gulp.task('test', function() {
    spawnSync(
        'python',
        [
            'manage.py',
            'test'
        ],
        {
            stdio: 'inherit'
        }
    );
});
