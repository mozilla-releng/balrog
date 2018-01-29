angular.module('app').controller('EnableUpdatesScheduledChangeCtrl',
  function($scope, $modalInstance, CSRF, sc, required_signoffs, EmergencyShutoffs, emergency_shutoff) {
    $scope.sc = angular.copy(sc);
    $scope.emergency_shutoff = emergency_shutoff;
    $scope.saving = false;
    $scope.auto_time = false;
    $scope.errors = {};

    $scope.toggleAutoTime = function(){
      if ($scope.auto_time){
        $("#btn__auto-time").addClass('active');
      }else{
        $('#btn__auto-time').removeClass('active');
      }
    };

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

    $scope.saveChanges = function() {
      $scope.saving = true;
      asap = new Date();
      asap.setMinutes(asap.getMinutes() + 5);
      $scope.sc.when = ($scope.auto_time) ? asap : $scope.sc.when;

      CSRF.getToken()
        .then(function(csrf_token) {
          sc = angular.copy($scope.sc);
          EmergencyShutoffs.scheduleEnableUpdates(sc, csrf_token)
            .success(function(response) {
              $scope.sc.sc_data_version = 1;
              $scope.sc.sc_id = response.sc_id;
              $scope.sc.signoffs = response.signoffs;
              $modalInstance.close($scope.sc);
              sweetAlert(
                "Schedule for enable updates",
                "Updates was scheduled to be enabled successfully.",
                "success");
            })
            .error(function(response, status) {
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

    $scope.deleteScheduledChange = function() {
      CSRF.getToken()
        .then(function(csrf_token) {
          sc = $scope.emergency_shutoff.scheduled_change;
          EmergencyShutoffs.deleteScheduledEnableUpdates(
            sc.sc_id, sc.data_version, csrf_token)
              .success(function(response) {
                $modalInstance.close(null);
                sweetAlert(
                  "Deleting Scheduled Changes",
                  "Scheduled Changes deleted successfully",
                  "success"
                );
              })
              .error(function(response) {
                sweetAlert(
                  "Deleting Scheduled Changes",
                  "Error on delete scheduled change",
                  "error"
                );
              });
        });
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
});