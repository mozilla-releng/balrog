angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         current_required_signoffs, pending_required_signoffs) {
  var roles = [{"role": "bbbb", "signoffs_required": null}];

  $controller("BaseRequiredSignoffCtrl", {
    $scope: $scope,
    $modalInstance: $modalInstance,
    $q: $q,
    CSRF: CSRF,
    ProductRequiredSignoffs: ProductRequiredSignoffs,
    PermissionsRequiredSignoffs: PermissionsRequiredSignoffs,
    current_required_signoffs: current_required_signoffs,
    pending_required_signoffs: pending_required_signoffs,
    roles: roles,
  });
});
