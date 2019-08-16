angular.module('app').controller('ReleaseReadOnlyCtrl',
function ($scope, $modalInstance, CSRF, Releases, release) {

  $scope.release = release;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    var data = $scope.release;
    data.read_only = release.read_only ? "" : true;

    CSRF.getToken()
    .then(function(csrf_token) {
      Releases.changeReadOnly($scope.release.name, data, csrf_token)
      .success(function(response) {
        $scope.release.data_version = response.new_data_version;
        $scope.release.read_only = data.read_only;
        $scope.saving = false;
        $modalInstance.close();
      })
      .error(function(response) {
        if (typeof response === 'object') {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        }
      })
      .finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
  };
});
