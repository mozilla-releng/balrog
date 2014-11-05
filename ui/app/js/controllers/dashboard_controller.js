angular.module("app").controller('DashboardController',
function($scope, $location, cssInjector, $localForage) {
  cssInjector.add('http://fonts.googleapis.com/css?family=Bangers');

  $scope.saved_searches = [];
  $localForage.getItem('savedSearches')
  .then(function(data) {
    if (data) {
      $scope.saved_searches = data;
    }
  });

  $scope.gotoSavedSearch = function(search) {
    $location.path(search.path);
    $location.hash(search.hash);
  };

});
