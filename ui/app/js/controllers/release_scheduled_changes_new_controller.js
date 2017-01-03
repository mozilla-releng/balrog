angular.module("app").controller("NewReleaseScheduledChangeCtrl",
function($scope, $http, $modalInstance, CSRF, Releases, scheduled_changes, sc) {


  $scope.is_edit = false;
  $scope.scheduled_changes = scheduled_changes;
  $scope.sc = sc;
  $scope.errors = {};
  $scope.saving = false;
  $scope.calendar_is_open = false;
  
  $scope.products = [];
  Releases.getProducts().success(function(response) {
    $scope.products = response.product;
  });


  $scope.setWhen = function(newDate) {
    if (!newDate) {
      newDate = new Date($("#id_when")[0].value);
      $scope.sc.when = newDate;
    }
    $scope.calendar_is_open = false;
    if (newDate <= new Date()) {
      $scope.errors.when = ["Scheduled time cannot be in the past"];
      $scope.sc.when = null;
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
    $scope.sc.name = "";

    var reader = new FileReader();
    reader.onloadend = function(evt) {
      var blob = evt.target.result;
      $scope.$apply( function() {
        try{
          var name = JSON.parse(blob).name;
          if (name) {
            $scope.sc.name = name;
          }
          else {
            $scope.errors.data = ["Form submission error", "Missing name field in JSON blob.\n"];
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
    if (!$scope.sc.product.trim()) {
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

    if (!$scope.sc.name.trim()) {
      sweetAlert(
        "Form Error",
        "Name is required",
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
        var data = angular.copy($scope.sc);
        data.blob = blob;
        Releases.addScheduledChange(data, csrf_token)
        .success(function(response){
          $scope.sc.sc_data_version = 1;
          $scope.sc.sc_id = response.sc_id;
          $scope.scheduled_changes.push($scope.sc);
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
      // should work
    reader.readAsText(file);

  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

