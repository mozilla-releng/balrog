angular.module("app").run(function($location, Auth0) {
  if (localStorage.getItem('isLoggedIn') === 'true') {
    Auth0.renewTokens();
  }
  else {
    Auth0.handleAuthentication(function(uri) {
      $location.path(uri).hash(null);
    },
    function(errMsg) {
      sweetAlert("Error logging in", errMsg, "error");
    });
  }
});
