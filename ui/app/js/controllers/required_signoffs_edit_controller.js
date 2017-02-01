angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
         required_signoffs, mode, product, channel) {
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
    editing: true,
  });
});
