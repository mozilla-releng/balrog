angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, Permissions, object_name, service, current_user, user_roles, required_signoffs, sc, pk, data) {
  $scope.saving = false;
  $scope.errors = {};
  $scope.object_name = object_name;
  $scope.sc = sc;
  $scope.pk = pk;
  $scope.data = data;
  $scope.current_user = current_user;
  $scope.signoff_role = null;
  $scope.possible_roles = [];
  // Only put Roles that this Scheduled Change requires as options.
  user_roles.forEach(function(role) {
    if (role in required_signoffs) {
      $scope.possible_roles.push(role);
    }
    if ($scope.possible_roles.length > 0) {
      $scope.signoff_role = $scope.possible_roles[0];
    }
  });

  $scope.saveChanges = function () {
    if ($scope.signoff_role === null) {
      $scope.errors["exception"] = "No Role selected!";
      return;
    }
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"role": $scope.signoff_role, "csrf_token": csrf_token};
      service.signoffOnScheduledChange($scope.sc.sc_id, data)
      .success(function(response) {
        $scope.saving = false;
        $scope.sc["signoffs"][$scope.current_user] = $scope.signoff_role;
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
