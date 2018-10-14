angular.module('app').controller('ReleaseDataCtrl',
function($scope, $http, $modalInstance, Releases, History, release, diff) {
  $scope.release = release;
  $scope.diff = diff;

  if (release.change_id) {
    if (diff) {
      const Diff = !!release.sc_id ? History.getScheduedReleaseDiff : Releases.getDiff;
       Diff.call(this, release.change_id).then(function(response) {
        $scope.release.diff = response.data;
      });

    } else {
      Releases.getData(release.change_id)
      .then(function(response) {
        $scope.release.data = response.data;
      });
    }

  } else {
    Releases.getRelease(release.name)
    .then(function(response) {
      $scope.release.data = response.data;
    });
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
