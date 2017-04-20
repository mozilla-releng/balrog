angular.module('app').controller('RevokeSignoffCtrl',
function ($scope, $modalInstance, CSRF, object_name, service, current_user, sc, pk, data) {
  $scope.saving = false;
  $scope.object_name = object_name;
  $scope.current_user = current_user;
  $scope.sc = sc;
  $scope.pk = pk;
  $scope.data = data;
  $scope.role = $scope.sc["signoffs"][current_user];

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"csrf_token": csrf_token};
      service.revokeSignoffOnScheduledChange($scope.sc.sc_id, data)
      .success(function(response) {
        $scope.saving = false;
        delete $scope.sc["signoffs"][$scope.current_user];
        $modalInstance.close();
      })
      .error(function(response) {
        $scope.saving = false;
        if (typeof response === "object") {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        }
        else {
          sweetAlert(
            "Unknown error:",
            response
          );
        }
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
