angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         required_signoffs, current_user) {
  var current_roles = [{"name": "", "data_version": null, "signoffs_required": null, "sc": null}];
  $controller("BaseRequiredSignoffCtrl", {
    $scope: $scope,
    $modalInstance: $modalInstance,
    $q: $q,
    CSRF: CSRF,
    ProductRequiredSignoffs: ProductRequiredSignoffs,
    PermissionsRequiredSignoffs: PermissionsRequiredSignoffs,
    required_signoffs: required_signoffs,
    // For some reason, setting these as defaults in BaseRequiredSignoffCtrl
    // doesn't work (we're unable to override them). Maybe something to do
    // with magical dependency injection.
    mode: "channel",
    product: "",
    channel: "",
    current_user: current_user,
    current_roles: current_roles,
    editing: false,
  });
});
