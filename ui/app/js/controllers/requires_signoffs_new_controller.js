angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, required_signoffs) {
  $scope.product = "";
  $scope.channel = "";
  $scope.required_signoff = {
    "channels": {},
    "permissions": {},
  };

  $scope.saveChanges = function() {
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
