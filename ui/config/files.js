/* Exports a function which returns an object that overrides the default &
 *   plugin file patterns (used widely through the app configuration)
 *
 * To see the default definitions for Lineman's file paths and globs, see:
 *
 *   - https://github.com/linemanjs/lineman/blob/master/config/files.coffee
 */
module.exports = function(lineman) {
  //Override file patterns here
  return {
    js: {
      vendor: [
        "vendor/js/angular.js",
        "vendor/js/angular-route.min.js",
        "vendor/js/angular-sanitize.min.js",
        "vendor/js/jquery-2.1.1.min.js",
        "vendor/js/ui-bootstrap-tpls-0.11.2.min.js",
        "vendor/js/lodash.min.js",
        "vendor/js/moment.min.js",
        "vendor/js/sweet-alert.min.js",
        "vendor/js/angular-css-injector.min.js",
        "vendor/bootstrap/js/bootstrap.min.js",

        "vendor/js/localforage.min.js",
        "vendor/js/angular-localForage.min.js",

        "vendor/js/datetimepicker.js",

        "vendor/js/auth0.js",
        "vendor/js/angular-auth0.js",
      ],
      app: [
        "app/js/app.js",
        "app/js/**/*.js"
      ]
    },

    css: {
      vendor: [
        "vendor/bootstrap/css/bootstrap.min.css",
        "vendor/css/**/*.css",
      ],
      app: "app/css/**/*.css",
      concatenated: "generated/css/app.css",
      minified: "dist/css/app.css",
      minifiedWebRelative: "css/app.css",
    },

    less: {
      compile: {
        options: {
          paths: [
            "vendor/css/**/*.css",
            "app/css/**/*.less"
          ]
        }
      }
    }
  };
};
