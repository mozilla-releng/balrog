angular.module('app').controller('EnableUpdatesCtrl',
  function($scope, $modalInstance, CSRF, EmergencyShutoffs, emergency_shutoff, signoffs_requirements){
    $scope.saving = false;
    $scope.emergency_shutoff = emergency_shutoff;
    $scope.signoffs_requirements = signoffs_requirements.filter(function(required_signoff) {
      return required_signoff.product === emergency_shutoff.product && required_signoff.channel === emergency_shutoff.channel;
    }).reduce(function(signoffs_reqs, signoff) {
      signoffs_reqs.length++;
      signoffs_reqs.roles[signoff.role] = signoff.signoffs_required;
      return signoffs_reqs;
    }, {'length': 0, 'roles': {}});

    $scope.enableUpdates = function() {
      $scope.saving = true;
      CSRF.getToken()
        .then(function(csrf_token) {
          if($scope.signoffs_requirements.length > 0) {
            EmergencyShutoffs.scheduleEnableUpdates($scope.emergency_shutoff, csrf_token)
              .success(function(response) {
                $modalInstance.close();
                sweetAlert(
                  "Enabling Updates",
                  "Updates have been scheduled to be enabled successfully.",
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
          } else {
            EmergencyShutoffs.delete(
              $scope.emergency_shutoff.product,
              $scope.emergency_shutoff.channel,
              $scope.emergency_shutoff.data_version,
              csrf_token)
                .success(function(response) {
                  $modalInstance.close();
                  sweetAlert(
                    "Enabling Updates",
                    "Updates were enabled successfully.",
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
          }
        });
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  });