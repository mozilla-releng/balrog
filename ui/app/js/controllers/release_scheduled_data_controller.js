angular.module('app').controller('ScheduledReleaseDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, release, diff) {
  $scope.release = release;
  $scope.diff = diff;

  if (release.change_id) {
    if (diff) {
      Releases.getDiff(release.change_id)
      .then(function(response) {
        $scope.release.diff = response.data;
      });

    } else {
      Releases.getScheduledData(release.change_id)
      .then(function(response) {
        $scope.release.data = response.data;
      });
    }

  } else {
    Releases.getScheduledChange(release.name)
    .then(function(response) {
      $scope.release.data = response.data;
    });
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
