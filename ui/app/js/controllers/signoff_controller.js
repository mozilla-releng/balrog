angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, Permissions, object_name, service, sc_id, pk, data, details) {
  $scope.saving = false;
  $scope.errors = {};
  $scope.object_name = object_name;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  $scope.data = data;
  $scope.details = details;
  $scope.signoff_role = null;

  $scope.current_user = null;
  $scope.user_roles = [];

  Permissions.getCurrentUser()
  .success(function(response) {
    $scope.user_roles = Object.keys(response["roles"]);
    $scope.current_user = response["username"];
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load current user Roles:",
      response
    );
  });

  $scope.saveChanges = function () {
    console.log($scope.signoff_role);
    if ($scope.signoff_role === null) {
      $scope.errors["exception"] = "No Role selected!";
      return;
    }
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"role": $scope.signoff_role, "csrf_token": csrf_token};
      service.signoffOnScheduledChange($scope.sc_id, data)
      .success(function(response) {
        $scope.saving = false;
        // update list of signoffs that have been made
        $scope.details["signoffs"][$scope.current_user] = $scope.signoff_role;
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
