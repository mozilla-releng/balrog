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
  $scope.products = [];
  Releases.getProducts().success(function(response) {
    $scope.products = response.product;
  });

  $scope.errors = {};
  $scope.saving = false;

  $scope.fillName = function () {
    var file = $scope.dataFile;
    $scope.errors.data = [];
    $scope.release.name = "";

    var reader = new FileReader();
    reader.onloadend = function(evt) {
      var blob = evt.target.result;
      $scope.$apply( function() {
        var name = JSON.parse(blob).name;
        if (name) {
           $scope.release.name = name;
        }
        else {
          $scope.errors.data = ["Form submission error", "Missing name field in JSON blob.\n"];
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
      $scope.saving = false;
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
