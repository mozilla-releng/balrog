angular.module('app').controller('EnableUpdatesCtrl',
  function($scope, $modalInstance, CSRF, EmergencyShutoffs, emergency_shutoff){
    $scope.saving = false;
    $scope.emergency_shutoff = emergency_shutoff;

    $scope.enableUpdates = function() {
      $scope.saving = true;
      CSRF.getToken()
        .then(function(csrf_token) {
          EmergencyShutoffs.delete(
            $scope.emergency_shutoff.product,
            $scope.emergency_shutoff.channel,
            $scope.emergency_shutoff.data_version,
            csrf_token)
              .success(function(response) {
                $modalInstance.close();
                sweetAlert(
                  "Enabling Updates",
                  "Updates was enabled successfully.",
                  "success");
              })
              .error(function(response, status) {
                if (typeof response === 'object') {
                  sweetAlert("Form submission error", response.data, "error");
                }
              })
              .finally(function(){
                $scope.saving = false;
              });
        });
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  });