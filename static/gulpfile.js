var gulp = require('gulp');
var pug = require('gulp-pug');
var sass = require('gulp-sass');

/* Copy root static assets (favicon, robots.txt, etc.) */
gulp.task('static', function() {
    return gulp.src('src/static/*.*')
        .pipe(gulp.dest('public/'));
});

/* Compile the source code for pug files */
gulp.task('pug', function() {
    return gulp.src('src/views/*.pug')
       .pipe(pug({
        pretty: true
     }))
       .pipe(gulp.dest('./public'))
});

/* Compile Sass Files */
gulp.task('sass', function() {
    return gulp.src('./src/sass/*.sass')
      .pipe(sass({
        errLogToConsole: true,
        outputStyle: 'compressed',
    }).on('error', sass.logError))
      .pipe(gulp.dest('./public/'))
})

gulp.task('default', ['static', 'pug', 'sass'], function() {
});
