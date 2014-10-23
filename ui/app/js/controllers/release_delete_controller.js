angular.module('app').controller('ReleaseDeleteCtrl',
function ($scope, $modalInstance, CSRFService, ReleasesService, release, releases) {

  $scope.release = release;
  $scope.releases = releases;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRFService.getToken()
    .then(function(csrf_token) {
      ReleasesService.deleteRelease($scope.release.name, $scope.release, csrf_token)
      .success(function(response) {
        $scope.releases.splice($scope.releases.indexOf($scope.release), 1);
        $modalInstance.close();
      })
      .error(function() {
        console.error(arguments);
      }).finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
