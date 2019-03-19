/*global: sweetAlert */

angular.module("app").controller('LoginController', function($window, Auth0) {
    // have to pass some sort of state, otherwise auth0 sets something that we don't know the value of!
    // This must match the state passed to login in the Auth0LoginController
    Auth0.handleAuthentication("balrogstate", function() {
      $window.close();
    },
    // We explicitly don't close the window when the login fails to avoid losing error messages.
    function(errMsg) {
      sweetAlert("Error logging in", errMsg, "error");
    });
});
