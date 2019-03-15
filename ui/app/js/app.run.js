angular.module("app").run(function($location, $http, Auth0) {
  handleError = function(errMsg) {
    sweetAlert("Error logging in", errMsg, "error");
  };
  // If a user has logged in previously, refresh their access token
  if (localStorage.getItem("isLoggedIn") === "true") {
    Auth0.renewTokens(handleError);
  }
  // If not, we might have just gotten back from a login through Auth0
  // TODO: can this block have to LoginController?
  else {
    Auth0.handleAuthentication(function(uri) {
      $location.path(uri).hash(null);
    },
    handleError);
  }
  // TODO: the angular sample code does this, but the timeout is always calculated as NaN for this call?
  // probably because renewTokens or handleAuthentication needs to complete first?
  // maybe this isn"t needed, seems to do nothing
  Auth0.scheduleRenewal();

  // Ensure that the bearer token is always included in requests to the backend.
  $http.defaults.headers.post.Authorization = "Bearer " + localStorage.getItem("accessToken");
  $http.defaults.headers.put.Authorization = "Bearer " + localStorage.getItem("accessToken");
  $http.defaults.headers.delete = {
    "Authorization": "Bearer " + localStorage.getItem("accessToken")
  };
});
