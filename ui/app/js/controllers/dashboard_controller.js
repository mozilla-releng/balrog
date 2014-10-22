angular.module("app").controller('DashboardController',
function($scope, $location, cssInjector) {
  cssInjector.add('http://fonts.googleapis.com/css?family=Bangers');
  //<link href='http://fonts.googleapis.com/css?family=Bangers' rel='stylesheet' type='text/css'>
  // document.createElement('link');

  // $scope.credentials = { username: "", password: "" };
  //
  // var onLoginSuccess = function() {
  //   $location.path('/home');
  // };
  //
  // $scope.login = function() {
  //   AuthenticationService.login($scope.credentials).success(onLoginSuccess);
  // };
});
