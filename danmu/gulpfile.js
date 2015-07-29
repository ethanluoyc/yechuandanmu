var gulp = require('gulp'),
    livereload = require('gulp-livereload');

gulp.task('default', ['watch']);

gulp.task('watch', function() {
    livereload.listen({basePath:'static'});
    gulp.watch('*.js', ['copyDanmu']);
});

gulp.task('copyDanmu', function(){
    gulp.src('*.js').pipe(gulp.dest('../static/danmu'));
    // .pipe(livereload({basePath:'static'}));
});
