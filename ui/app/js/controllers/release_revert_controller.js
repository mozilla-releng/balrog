/*global sweetAlert */

angular.module('app').controller('ReleaseRevertCtrl',
function ($scope, $modalInstance, CSRFService, Releases, release) {

  $scope.release = release;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRFService.getToken()
    .then(function(csrf_token) {
      // console.log($scope.release.name, )
      Releases.revertRelease($scope.release.name, $scope.release.change_id, csrf_token)
      .success(function(response) {
        $scope.saving = false;
        $modalInstance.close();
      })
      .error(function(response, status) {
        $scope.saving = false;
        console.error(status, response);
        sweetAlert(
          "Unknown Error (" + status + ")",
          "Unable to save\n" +
          "(" + response + ")",
          "error"
        );
        // console.error(arguments);
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
