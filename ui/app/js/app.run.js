angular.module("app").run(function(Auth0) {
  if (localStorage.getItem('isLoggedIn') === 'true') {
    Auth0.renewTokens();
  }
  else {
    Auth0.handleAuthentication();
  }
});
