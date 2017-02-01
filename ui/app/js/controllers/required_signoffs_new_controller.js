angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         current_required_signoffs, pending_required_signoffs) {
  var roles = [{"role": "", "signoffs_required": null}];

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
    // For some reason, setting these as defaults in BaseRequiredSignoffCtrl
    // doesn't work (we're unable to override them). Maybe something to do
    // with magical dependency injection.
    mode: "channel",
    product: "",
    channel: "",
    editing: false,
  });
});
