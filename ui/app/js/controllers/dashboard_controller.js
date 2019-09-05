angular.module("app").controller('DashboardController',
function($scope, $location, cssInjector, $localForage, Page, Auth0, NewBalrogURL) {
  cssInjector.add('//fonts.googleapis.com/css?family=Bangers');

  Page.setTitle('Home');

  $scope.new_ui_url = NewBalrogURL;
  $scope.auth0 = Auth0;
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
