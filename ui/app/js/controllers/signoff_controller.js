angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, Permissions, title, service, sc_id, pk, details) {
  $scope.saving = false;
  $scope.title = title;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  $scope.details = details;
  $scope.signoff_role = null;

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
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
