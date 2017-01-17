
angular.module('app').controller('EditReleaseScheduledChangeCtrl',
function ($scope, $modalInstance, CSRF, Releases, sc) {

  $scope.is_edit = true;
  $scope.original_sc = sc;
  $scope.sc = angular.copy(sc);
  $scope.products = [];
  Releases.getProducts().success(function(response) {
    $scope.products = response.product;
  });

  $scope.errors = {};
  $scope.saving = false;

  $scope.setWhen = function(newDate) {
    if (!newDate) {
      newDate = new Date($("#id_when")[0].value);
      $scope.sc.when = newDate;
    }
    $scope.calendar_is_open = false;
    if (newDate <= new Date()) {
      $scope.errors.when = ["Scheduled time cannot be in the past"];
      $scope.sc.when = $scope.original_sc.when;
    }
    else {
      $scope.errors.when = null;
    }
  };

  $scope.clearWhen = function () {
    $scope.sc.when = null;
    $scope.errors.when = null;
  };

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
          else if (name !== $scope.sc.name) {
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
    if($scope.sc.change_type!=="delete") {
      if (!$scope.sc.product.trim()) {
        sweetAlert(
          "Form Error",
          "Product is required.",
          "error"
        );
        return;
      }
      if (!$scope.dataFile) {
        $scope.sc.data = $scope.sc.data;
      } else {
        var file = $scope.dataFile;

        var reader = new FileReader();
        reader.onload = function(evt) {
        $scope.sc.data = evt.target.result;
        };
      // should work
      reader.readAsText(file);
      }
      if (!$scope.sc.name.trim()) {
        sweetAlert(
          "Form Error",
          "Name is required",
          "error"
        );
        return;
      }
    } 

    $scope.saving = true;


      CSRF.getToken()
      .then(function(csrf_token) {
        var data = $scope.sc;
        Releases.updateScheduledChange($scope.sc.sc_id, data, csrf_token)
        .success(function(response) {
          $scope.sc.data_version = response.new_data_version;
          angular.copy($scope.sc, $scope.original_sc);
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
    


  }; // /saveChanges

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
