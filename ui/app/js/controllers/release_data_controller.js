angular.module('app').controller('ReleaseDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, release, diff, previous_version) {
  $scope.release = release;
  $scope.diff = diff;
  $scope.previous_version = previous_version;

  if (release.timestamp) {
    if (diff) {
      if (previous_version) {
        Releases.getData(release.data_url)
        .then(function(data) {
          Releases.getData(previous_version.data_url)
          .then(function(previous_data) {
            $scope.release.diff = JsDiff.createTwoFilesPatch(
              "Data Version " + previous_version.data_version,
              "Data Version " + release.data_version,
              previous_data,
              data
            );
          });
        });
      }
      else {
        Releases.getData(release.data_url)
        .then(function(data) {
          $scope.release.diff = JsDiff.createTwoFilesPatch(null, "Data Version " + release.data_version, "", data);
        });
      }
    } else {
      Releases.getData(release.data_url)
      .then(function(data) {
        $scope.release.data = data;
      });
    }

  } else {
    Releases.getRelease(release.name)
    .then(function(response) {
      $scope.release.data = stringify(response.data, { cmp: function(a, b) { return a.key < b.key ? -1 : 1; }, space: 2});
    });
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
