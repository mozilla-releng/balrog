angular.module("app").controller('NavController', function($scope, $location) {
  $scope.isOn = function(path) {
    if (path === '/') {
      return $location.path() === path;
    } else {
      // startswith
      return $location.path().substr(0, path.length) === path;
    }
  };
});
