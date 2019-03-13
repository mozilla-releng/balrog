angular.module("app").run(function($location, Auth0) {
  handleError = function(errMsg) {
    sweetAlert("Error logging in", errMsg, "error");
  };
  if (localStorage.getItem('isLoggedIn') === 'true') {
    Auth0.renewTokens(handleError);
  }
  else {
    Auth0.handleAuthentication(function(uri) {
      $location.path(uri).hash(null);
    },
    handleError);
  }
  // TODO: the angular sample code does this, but the timeout is always calculated as NaN for this call?
  // probably because renewTokens or handleAuthentication needs to complete first?
  // maybe this isn't needed, seems to do nothing
  Auth0.scheduleRenewal();
});
