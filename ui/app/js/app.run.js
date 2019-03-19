angular.module("app").run(function($location, $http, Auth0) {
  handleError = function(errMsg) {
    sweetAlert("Error logging in", errMsg, "error");
  };
  // If a user has logged in previously, refresh their access token
  if (localStorage.getItem("isLoggedIn") === "true") {
    Auth0.renewTokens(handleError);
  }

  // Ensure that the bearer token is always included in requests to the backend.
  $http.defaults.headers.post.Authorization = "Bearer " + localStorage.getItem("accessToken");
  $http.defaults.headers.put.Authorization = "Bearer " + localStorage.getItem("accessToken");
  $http.defaults.headers.delete = {
    "Authorization": "Bearer " + localStorage.getItem("accessToken")
  };
});
