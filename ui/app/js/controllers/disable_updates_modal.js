angular.module('app').controller('DisableUpdatesModalCtrl',
  function($scope, $modalInstance, EmergencyShutoffs, product, channel){
    $scope.product = product;
    $scope.channel = channel;
    $scope.saving = false;

    $scope.disableUpdates = function() {
      $scope.saving = true;
      EmergencyShutoffs.create($scope.product, $scope.channel)
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
    };

    $scope.cancel = function() {
      $modalInstance.dismiss('cancel');
    };
  });
