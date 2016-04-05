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
      .error(function(response) {
         if (typeof response === 'object') {
          message = '';
          if (release.read_only) {
            message = 'Product is read only';
          }
          $scope.errors = response;
          sweetAlert(
            "Deletion error",
            message
          );
        } else if (typeof response === 'string') {
          // quite possibly an error in the blob validation
          sweetAlert(
            "Deletion error",
            "Unable to delete successfully.\n" +
            "(" + response+ ")",
            "error"
          );
        }
        console.error(response);
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
