angular.module("app").controller('LoginController', function($scope, Auth0) {
  if (localStorage.getItem('isLoggedIn') === 'true') {
    // TODO: do this every ~10min too
    Auth0.renewTokens();
  }
  else {
    Auth0.handleAuthentication();
  }
});
