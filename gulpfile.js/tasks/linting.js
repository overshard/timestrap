var gulp         = require('gulp');

var eslint       = require('gulp-eslint');
var sasslint     = require('gulp-sass-lint');

var spawn        = require('child_process').spawn;


gulp.task('lint', ['pythonlint', 'sasslint', 'eslint']);


gulp.task('pythonlint', function() {
    spawn(
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
        'gulpfile.js/**/*.js',
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
