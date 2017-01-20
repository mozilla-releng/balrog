angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.product = "";
  $scope.channel = "";
  $scope.new_roles = 1;

  $scope.addRole = function() {
    $scope.new_roles++;
  };

  $scope.saveChanges = function() {

  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
