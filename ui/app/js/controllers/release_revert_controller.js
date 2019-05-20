/*global sweetAlert */

angular.module('app').controller('ReleaseRevertCtrl',
function ($scope, $modalInstance, CSRF, Releases, release) {

  $scope.release = release;
  $scope.saving = false;

  Releases.getData(release.data_url)
  .then(function(data) {
    $scope.data = data;
  });

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      // console.log($scope.release.name, )
      data = {
        "name": $scope.release.name,
        "product": $scope.release.product,
        "blob": $scope.data,
        "data_version": $scope.release.data_version,
      };
      Releases.updateRelease($scope.release.name, data, csrf_token)
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
