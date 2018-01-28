angular.module('app').controller('DisableUpdatesModalCtrl',
  function($scope, $modalInstance, EmergencyShutoffs, product, channel){
    $scope.product = product;
    $scope.channel = channel;
    $scope.saving = false;

    $scope.disableUpdates = function() {
      $scope.saving = true;
      EmergencyShutoffs.createEmergencyShutoff($scope.product, $scope.channel)
        .success(function(response) {
          $modalInstance.close(response);
        })
        .error(function(response, status) {
          console.log(response);
          if (typeof response === 'object') {
            sweetAlert(
              "Form submission error",
              response.data,
              "error"
            );
          }
        })
        .finally(function() {
          $scope.saving = false;
        });
    };

    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  });