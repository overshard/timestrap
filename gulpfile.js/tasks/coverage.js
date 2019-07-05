const gulp = require("gulp");

const del = require("del");

const spawn = require("child_process").spawn;

gulp.task(
  "coverage:test",
  gulp.series("build:webpack:production", () => {
    let command = [
      "run",
      "coverage",
      "run",
      "--parallel-mode",
      "--concurrency=multiprocessing",
      "--rcfile=.coveragerc",
      "manage.py",
      "test",
      "--parallel"
    ];

    return spawn("pipenv", command, { stdio: "inherit" });
  })
);

gulp.task("coverage:combine", () => {
  return spawn("pipenv", ["run", "coverage", "combine"], { stdio: "inherit" });
});

gulp.task("coverage:report", () => {
  return spawn(
    "pipenv",
    ["run", "coverage", "report", "-m", "--rcfile=.coveragerc"],
    { stdio: "inherit" }
  );
});

gulp.task("coverage:coveralls", () => {
  return spawn("pipenv", ["run", "coveralls"], { stdio: "inherit" });
});

gulp.task("coverage:clean", () => {
  return del([
    "client/static/**/*",
    "geckodriver.log",
    ".coverage*",
    "!.coveragerc"
  ]);
});

gulp.task(
  "coverage:development",
  gulp.series(
    "lint",
    "coverage:test",
    "coverage:combine",
    "coverage:report",
    "coverage:clean"
  )
);

gulp.task(
  "coverage:production",
  gulp.series(
    "lint",
    "coverage:test",
    "coverage:combine",
    "coverage:report",
    "coverage:coveralls"
  )
);
