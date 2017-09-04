angular.module("app").controller("NewReleaseScheduledDeleteCtrl",
function($scope, $http, $modalInstance, CSRF, Releases, scheduled_changes, sc) {


  $scope.is_edit = false;
  $scope.scheduled_changes = scheduled_changes;
  $scope.sc = sc;
  $scope.errors = {};
  $scope.saving = false;
  $scope.calendar_is_open = false;
  $scope.auto_time = false;



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


 $scope.changeName = function () {
    //wait for actual file to be loaded
    setTimeout($scope.fillName, 0);
  };

  $scope.saveChanges = function () {

    $scope.saving = true;
    $scope.errors = {};
    asap = new Date();
    asap.setMinutes(asap.getMinutes() + 5);
    $scope.sc.when = ($scope.auto_time) ? asap : $scope.sc.when;


      CSRF.getToken()
      .then(function(csrf_token) {
        var data = $scope.sc;
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
              "(" + response + ")",
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


  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

