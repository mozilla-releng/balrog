/*global: sweetAlert */

angular.module("app").controller('LoginController', function($scope, Auth0) {
  Auth0.handleAuthentication(function(errMsg) {
    sweetAlert("Error logging in", errMsg, "error");
  });
});
