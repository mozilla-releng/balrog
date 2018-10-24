angular.module('app').controller('DisableUpdatesModalCtrl',
  function($scope, $modalInstance, CSRF, EmergencyShutoffs, product, channel){
    $scope.product = product;
    $scope.channel = channel;
    $scope.saving = false;

    $scope.disableUpdates = function() {
      $scope.saving = true;
      CSRF.getToken().then(function(csrf_token) {
        EmergencyShutoffs.create($scope.product, $scope.channel, csrf_token)
          .success(function(response) {
            $modalInstance.close(response);
            sweetAlert("Disabling Updates", "Updates were disabled successfully!", "success");
          })
          .error(function(response, status) {
            if (typeof response === 'object') {
              sweetAlert("Form submission error", response.data, "error");
            }
          })
          .finally(function() {
            $scope.saving = false;
          });
        });
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
  });
