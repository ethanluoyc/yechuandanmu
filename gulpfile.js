/*eslint semi:["error", "always"] */
var gulp = require('gulp');
var livereload = require('gulp-livereload');
var eslint = require('gulp-eslint');
var jsx = require('gulp-jsx');


gulp.task('default', function() {
  console.log('hello world');
});

gulp.task('js', function() {
  gulp.src(['static/js/*.jsx'])
    .pipe(jsx({
      factory: 'React.createClass'
    }))
    .pipe(gulp.dest('dist'))
    .pipe(livereload());
});

gulp.task('lint', function() {
  gulp.src(['static/js/*.js', 'static/js/*jsx'])
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
