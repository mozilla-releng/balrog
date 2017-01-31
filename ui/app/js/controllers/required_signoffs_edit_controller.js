angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         current_required_signoffs, pending_required_signoffs, mode, product, channel) {
  var roles = [];
  // how to detect pending vs. current ?
  for (let role of Object.keys(current_required_signoffs[product]["channels"][channel])) {
    roles.push({
        "role": role,
        "signoffs_required": current_required_signoffs[product]["channels"][channel][role]["signoffs_required"],
    });
  }

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
    mode: mode,
    product: product,
    channel: channel,
  });
});
