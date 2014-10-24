/*global: sweetAlert */

angular.module('app').controller('ReleaseEditCtrl',
function ($scope, $modalInstance, CSRFService, Releases, release) {

  $scope.is_edit = true;
  $scope.original_release = release;
  $scope.release = angular.copy(release);

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    var file = $scope.dataFile;

    var reader = new FileReader();
    reader.onload = function(evt) {
      var blob = evt.target.result;

      CSRFService.getToken()
      .then(function(csrf_token) {
        var data = $scope.release;
        data.data = blob;  // it's an edit
        Releases.updateRelease($scope.release.name, data, csrf_token)
        .success(function(response) {
          $scope.release.data_version = response.new_data_version;
          angular.copy($scope.release, $scope.original_release);
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
          } else if (typeof response === 'string') {
            // quite possibly an error in the blob validation
            sweetAlert(
              "Form submission error",
              "Unable to submit successfully.\n" +
              "(" + response+ ")",
              "error"
            );
          }
        })
        .finally(function() {
          $scope.saving = false;
        });
      });
    };
    if (typeof file === 'undefined') {
      sweetAlert(
        "Form Error",
        "No file has been selected.",
        "error"
      );
      return;
    } else {
      // should work
      reader.readAsText(file);
    }

  }; // /saveChanges

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
