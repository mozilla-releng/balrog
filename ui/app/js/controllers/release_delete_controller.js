angular.module('app').controller('ReleaseDeleteCtrl',
function ($scope, $modalInstance, CSRF, Releases, release, releases) {

  $scope.release = release;
  $scope.releases = releases;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Releases.deleteRelease($scope.release.name, $scope.release, csrf_token)
      .success(function(response) {
        $scope.releases.splice($scope.releases.indexOf($scope.release), 1);
        $scope.saving = false;
        $modalInstance.close();
      })
      .error(function() {
        console.error(arguments);
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
