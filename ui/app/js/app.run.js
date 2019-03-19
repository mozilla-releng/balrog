angular.module("app").run(function($location, $http, Auth0) {
  // If a user has logged in previously, refresh their access token
  if (localStorage.getItem("isLoggedIn") === "true") {
    Auth0.renewTokens(function(errMsg) {
      sweetAlert("Error logging in", errMsg, "error");
    });
  }
});
