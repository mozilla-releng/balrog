angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         current_required_signoffs, pending_required_signoffs, mode, product, channel) {
  var roles = [];
  // how to detect pending vs. current ?
  var i = null;
  if (mode === "channel") {
    i = current_required_signoffs[product]["channels"][channel];
  }
  else if (mode === "permissions") {
    i = current_required_signoffs[product]["permissions"];
  }
  for (let role of Object.keys(i)) {
    roles.push({
        "role": role,
        "signoffs_required": i[role]["signoffs_required"],
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
    editing: true,
  });
});
