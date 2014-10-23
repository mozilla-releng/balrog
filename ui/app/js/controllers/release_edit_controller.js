angular.module('app').controller('ReleaseEditCtrl',
function ($scope, $modalInstance, CSRFService, ReleasesService, release) {

  $scope.original_release = release;
  $scope.release = angular.copy(release);

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRFService.getToken()
    .then(function(csrf_token) {
      ReleasesService.updateRelease($scope.release.name, $scope.release, csrf_token)
      .success(function(response) {
        $scope.release.data_version = response.new_data_version;
        angular.copy($scope.release, $scope.original_release);
        $scope.saving = false;
        $modalInstance.close();
      }).error(function(response) {
        if (typeof response === 'object') {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        }
      }).finally(function() {
        $scope.saving = false;
      });
    });

  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
