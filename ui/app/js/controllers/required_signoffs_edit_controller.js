angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         required_signoffs, mode, product, channel) {
  var current_roles = [];
  if (mode === "channel") {
    for (let role of Object.keys(required_signoffs[product]["channels"][channel])) {
      current_roles.push({
        "role": role,
        "data_version": required_signoffs[product]["channels"][channel][role]["data_version"],
        "sc_data_version": required_signoffs[product]["channels"][channel][role]["sc_data_version"],
        "signoffs_required": required_signoffs[product]["channels"][channel][role]["signoffs_required"],
        "sc_id": required_signoffs[product]["channels"][channel][role]["sc_id"],
      });
    }
  }
  else if (mode === "permissions") {
    for (let role of Object.keys(required_signoffs[product]["permissions"])) {
      current_roles.push({
        "role": role,
        "data_version": required_signoffs[product]["permissions"][role]["data_version"],
        "sc_data_version": required_signoffs[product]["permissions"][role]["sc_data_version"],
        "signoffs_required": required_signoffs[product]["permissions"][role]["signoffs_required"],
        "sc_id": required_signoffs[product]["permissions"][role]["sc_id"],
      });
    }
  }

  $controller("BaseRequiredSignoffCtrl", {
    $scope: $scope,
    $modalInstance: $modalInstance,
    $q: $q,
    CSRF: CSRF,
    ProductRequiredSignoffs: ProductRequiredSignoffs,
    PermissionsRequiredSignoffs: PermissionsRequiredSignoffs,
    required_signoffs: required_signoffs,
    mode: mode,
    product: product,
    channel: channel,
    current_roles: current_roles,
    editing: true,
  });
});
