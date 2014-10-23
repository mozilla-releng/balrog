angular.module('app').controller('ReleaseDataCtrl',
function($scope, $http, $modalInstance, ReleasesService, RulesService, release) {

  $scope.release = release;
  ReleasesService.getRelease(release.name)
  .then(function(response) {
    $scope.release.data = response.data;
  });

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
