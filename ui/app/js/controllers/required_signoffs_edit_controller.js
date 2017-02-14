angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         required_signoffs, mode, product, channel, current_user) {
  var current_roles = [];
  if (mode === "channel") {
    Object.keys(required_signoffs[product]["channels"][channel]).forEach(function(role) {
      current_roles.push({
        "role": role,
        "data_version": required_signoffs[product]["channels"][channel][role]["data_version"],
        "signoffs_required": required_signoffs[product]["channels"][channel][role]["signoffs_required"],
        "sc": required_signoffs[product]["channels"][channel][role]["sc"],
      });
    });
  }
  else if (mode === "permissions") {
    Object.keys(required_signoffs[product]["permissions"]).forEach(function(role) {
      current_roles.push({
        "role": role,
        "data_version": required_signoffs[product]["permissions"][role]["data_version"],
        "signoffs_required": required_signoffs[product]["permissions"][role]["signoffs_required"],
        "sc": required_signoffs[product]["permissions"][role]["sc"],
      });
    });
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
    current_user: current_user,
    current_roles: current_roles,
    editing: true,
  });
});
