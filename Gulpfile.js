var gulp         = require('gulp');

var concat       = require('gulp-concat');
var sass         = require('gulp-sass');
var sasslint     = require('gulp-sass-lint');
var autoprefixer = require('gulp-autoprefixer');
var riot         = require('gulp-riot');
var eslint       = require('gulp-eslint');

var spawn        = require('child_process').spawn;
var spawnSync    = require('child_process').spawnSync;


// Helpers
function manageSync(command) {
    var fullCommand = ['manage.py'].concat(command);
    spawnSync(
        'python',
        fullCommand,
        {
            stdio: 'inherit'
        }
    );
}


// Primary tasks for dealing with static files
gulp.task('styles', function() {
    var files = [
        'node_modules/font-awesome/css/font-awesome.min.css',
        'node_modules/tether/dist/css/tether.min.css',
        'node_modules/bootstrap/dist/css/bootstrap.min.css',
        'node_modules/select2/dist/css/select2.min.css',
        'node_modules/pickadate/lib/compressed/themes/default.css',
        'node_modules/pickadate/lib/compressed/themes/default.date.css',
        'timestrap/static_src/sass/**/*.scss'
    ];
    gulp.src(files)
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(concat('bundle.css'))
        .pipe(gulp.dest('timestrap/static/css/'));
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
        'node_modules/riot/riot.min.js',
        'node_modules/riot-route/dist/route.min.js',
        'timestrap/static_src/scripts/**/*.js'
    ];
    gulp.src(files)
        .pipe(concat('bundle.js'))
        .pipe(gulp.dest('timestrap/static/js/'));
});


gulp.task('tags', function() {
    var files = [
        'timestrap/static_src/tags/**/*.tag'
    ];
    gulp.src(files)
        .pipe(riot())
        .pipe(concat('bundle-tags.js'))
        .pipe(gulp.dest('./timestrap/static/js/'));
});


gulp.task('extras', function() {
    var files = [
        'node_modules/font-awesome/fonts/*'
    ];
    gulp.src(files)
        .pipe(gulp.dest('timestrap/static/fonts/'));
});


gulp.task('build', ['styles', 'scripts', 'tags', 'extras']);


gulp.task('watch', function() {
    gulp.watch('timestrap/static_src/sass/**/*.scss', ['styles']);
    gulp.watch('timestrap/static_src/scripts/**/*.js', ['scripts']);
    gulp.watch('timestrap/static_src/tags/**/*.tag', ['tags']);
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
    var pg_dump = spawn(
        'flake8',
        [
            '--exclude=venv,.venv,node_modules,migrations'
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
        'timestrap/static_src/scripts/**/*.js',
        'timestrap/static_src/tags/**/*.tag'
    ];
    gulp.src(files)
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
    manageSync(['makemigrations']);
});


gulp.task('migrate', function() {
    manageSync(['migrate']);
});


gulp.task('createsuperuser', function() {
    manageSync(['createsuperuser']);
});


gulp.task('reset', function() {
    manageSync(['flush', '--noinput']);
    manageSync(['heroku']);
    manageSync(['fake']);
});


// Testing tasks
gulp.task('test', function() {
    manageSync(['test']);
});


gulp.task('coverage', function() {
    spawnSync(
        'coverage',
        [
            'run',
            '--source=core,api',
            'manage.py',
            'test'
        ],
        {
            stdio: 'inherit'
        }
    );
    spawnSync(
        'coverage',
        [
            'report',
            '-m'
        ],
        {
            stdio: 'inherit'
        }
    );
});


// Documentation tasks
gulp.task('docs-github', function() {
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


gulp.task('docs-rtd', function() {
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


gulp.task('docs-watch', function() {
    gulp.watch(['docs/**/*.md', 'docs/**/*.rst'], ['docs-github', 'docs-rtd']);
});


gulp.task('docs', ['docs-github', 'docs-rtd', 'docs-watch']);
