angular.module('app').controller('ReleaseDataCtrl',
function($scope, $http, $modalInstance, ReleasesService, RulesService, release, diff) {

  $scope.release = release;
  $scope.diff = diff;

  if (release.change_id) {
    if (diff) {
      ReleasesService.getDiff(release.change_id)
      .then(function(response) {
        $scope.release.diff = response.data;
      });

    } else {
      ReleasesService.getData(release.change_id)
      .then(function(response) {
        $scope.release.data = response.data;
      });
    }

  } else {
    ReleasesService.getRelease(release.name)
    .then(function(response) {
      $scope.release.data = response.data;
    });
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
