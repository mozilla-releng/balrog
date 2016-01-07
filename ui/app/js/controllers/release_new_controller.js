/*global: sweetAlert */

angular.module('app').controller('NewReleaseCtrl',
function($scope, $http, $modalInstance, CSRF, Releases, releases) {

  $scope.is_edit = false;
  $scope.releases = releases;
  $scope.release = {
    name: '',
    product: '',
    version: ''
  };
  $scope.errors = {};
  $scope.saving = false;

  $scope.saveChanges = function () {
    if (!$scope.release.product.trim()) {
      sweetAlert(
        "Form Error",
        "Product is required.",
        "error"
      );
      return;
    }
    $scope.saving = true;
    $scope.errors = {};

    var file = $scope.dataFile;

    var reader = new FileReader();
    reader.onload = function(evt) {
      var blob = evt.target.result;
      CSRF.getToken()
      .then(function(csrf_token) {
        var data = $scope.release;
        data.blob = blob;
        Releases.addRelease(data, csrf_token)
        .success(function(response){
          $scope.release.data_version = response.new_data_version;
          $scope.releases.push($scope.release);
          $modalInstance.close();
        })
        .error(function(response){
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

  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
