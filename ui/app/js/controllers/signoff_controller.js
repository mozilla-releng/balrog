angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, Permissions, object_name, service, sc_id, pk, data, details) {
  $scope.saving = false;
  $scope.object_name = object_name;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  // todo: if details goes unused, rename data to details
  $scope.data = data;
  $scope.details = details;
  $scope.signoff_role = null;

  $scope.current_user = null;
  $scope.user_roles = [];

  $scope.$watch("user_roles", function() {
    if ($scope.signoff_role === null) {
      if ($scope.user_roles.length > 0) {
        $scope.signoff_role = $scope.user_roles[0];
      }
    }
  }, true);

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
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      var data = {"role": $scope.signoff_role, "csrf_token": csrf_token};
      service.signoffOnScheduledChange($scope.sc_id, data)
      .success(function(response) {
        // update list of signoffs that have been made
        $scope.details["signoffs"]["username"] = $scope.current_user;
        //$modalInstance.close();
      })
      .error(function(response, status) {
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
