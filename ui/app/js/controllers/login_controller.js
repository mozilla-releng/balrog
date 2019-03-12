/*global: sweetAlert */

angular.module("app").controller('LoginController', function($scope, $location, Auth0) {
  Auth0.handleAuthentication(function(uri) {
    $location.path(uri).hash(null);
  },
  function(errMsg) {
    sweetAlert("Error logging in", errMsg, "error");
  });
});
