/*global: sweetAlert */

angular.module("app").controller('LoginController', function($window, Auth0) {
    // have to pass some sort of state, otherwise auth0 sets something that we don't know the value of!
    Auth0.handleAuthentication("fakestate", function() {
      $window.close();
    },
    function(errMsg) {
      sweetAlert("Error logging in", errMsg, "error");
    });
});
