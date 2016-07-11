/*eslint semi:["error", "always"] */
const gulp = require('gulp');
const livereload = require('gulp-livereload');
const eslint = require('gulp-eslint');
const babel = require('gulp-babel');
const sourcemaps = require('gulp-sourcemaps');
const environments = require('gulp-environments');

var dev = environments.development;
var prod = environments.productions;


gulp.task('default',['js']);

gulp.task('js', function() {
  gulp.src(['static/js/src/*.jsx'])
    .pipe(dev(sourcemaps.init()))
    .pipe(babel({presets: ['react']}))
    .pipe(dev(sourcemaps.write('.')))
    .pipe(gulp.dest('static/js/build/'))
    .pipe(livereload());
  gulp.src(['static/js/src/*.js'])
    .pipe(gulp.dest('static/js/build'));
});

gulp.task('lint', function() {
  gulp.src(['static/js/src/*.js', 'static/js/src/*jsx'])
    .pipe(eslint({
      'configFile': '.eslintrc'
    }))
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

gulp.task('livereload', function() {
  livereload.listen({start: true});
  gulp.watch(['static/js/*.js', 'static/js/*jsx'], ['js']);
});
