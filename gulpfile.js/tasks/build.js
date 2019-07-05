const gulp = require("gulp");

const del = require("del");

const webpack = require("webpack");
const webpackStream = require("webpack-stream");

const webpackConfig = require("../../webpack.config.js");

gulp.task("build:clean", () => {
  return del(["client/static/**/*"]);
});

gulp.task("build:webpack:development", () => {
  webpackConfig.mode = "development";
  webpackConfig.watch = true;

  return gulp
    .src("client/static_src/main.js")
    .pipe(webpackStream(webpackConfig, webpack))
    .on("error", function handleError() {
      this.emit("end");
    })
    .pipe(gulp.dest("client/static/"));
});

gulp.task("build:webpack:production", () => {
  return gulp
    .src("client/static_src/main.js")
    .pipe(webpackStream(webpackConfig, webpack))
    .pipe(gulp.dest("client/static/"));
});

gulp.task(
  "build:development",
  gulp.series("build:clean", "build:webpack:development")
);

gulp.task(
  "build:production",
  gulp.series("build:clean", "build:webpack:production")
);
