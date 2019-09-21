'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var bourbon = require('bourbon').includePaths;

sass.compiler = require('node-sass');

gulp.task('sass', function () {
  return gulp.src('./static/blog/scss/*.scss')
    .pipe(sass({
      includePaths: [bourbon]
    }))
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest('./static/blog/css'));
});

gulp.task('sass:watch', function () {
  gulp.watch('./static/blog/scss/*.scss', ['sass']);
});
