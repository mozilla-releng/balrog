angular.module('app').controller('RevokeSignoffCtrl',
function ($scope, $modalInstance, CSRF, object_name, service, current_user, sc_id, pk, data, details) {
  $scope.saving = false;
  $scope.object_name = object_name;
  $scope.current_user = current_user;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  $scope.data = data;
  $scope.details = details;
  $scope.role = details["signoffs"][current_user];

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"csrf_token": csrf_token};
      service.revokeSignoffOnScheduledChange($scope.sc_id, data)
      .success(function(response) {
        $scope.saving = false;
        delete $scope.details["signoffs"][$scope.current_user];
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
