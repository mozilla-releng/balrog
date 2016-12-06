/*global: sweetAlert */

angular.module('app').controller('ReleaseEditCtrl',
function ($scope, $modalInstance, CSRF, Releases, release) {

  $scope.is_edit = true;
  $scope.original_release = release;
  $scope.release = angular.copy(release);
  $scope.products = [];
  Releases.getProducts().success(function(response) {
    $scope.products = response.product;
  });

  $scope.errors = {};
  $scope.saving = false;
  
  $scope.fillName = function () {
    var file = $scope.dataFile;
    $scope.errors.data = [];
    var reader = new FileReader();
    reader.onloadend = function(evt) {
      var blob = evt.target.result;
      $scope.$apply( function() {
        try {
          var name = JSON.parse(blob).name;
          if(!name) {
            $scope.errors.data = ["Form submission error", "Name missing in blob.\n"];
          }
          else if (name !== $scope.release.name) {
            $scope.errors.data = ["Form submission error", "Name differs compared to name in blob.\n"];
          }
        }catch(err) {
          $scope.errors.data = ["Form submission error", "Malformed JSON file.\n"];
        }
      });
    };
    if (typeof file !== 'undefined') {
      // should work
      reader.readAsText(file);
    }

  };

  $scope.changeName = function () {
    //wait for actual file to be loaded
    setTimeout($scope.fillName, 0);
  };

  $scope.saveChanges = function () {
    if (!$scope.release.product.trim()) {
      sweetAlert(
        "Form Error",
        "Product is required.",
        "error"
      );
      return;
    }
    if (!$scope.dataFile) {
      sweetAlert(
        "Form Error",
        "No file has been selected.",
        "error"
      );
      return;
    }
    if (!$scope.release.name.trim()) {
      sweetAlert(
        "Form Error",
        "Name is required",
        "error"
      );
      return;
    }

    $scope.saving = true;

    var file = $scope.dataFile;

    var reader = new FileReader();
    reader.onload = function(evt) {
      var blob = evt.target.result;

      CSRF.getToken()
      .then(function(csrf_token) {
        var data = $scope.release;
        data.blob = blob;
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
    // should work
    reader.readAsText(file);

  }; // /saveChanges

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
