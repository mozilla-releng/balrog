angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $controller, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, required_signoffs) {
  $controller("BaseRequiredSignoffCtrl", {
    $scope: $scope,
    $modalInstance: $modalInstance,
    $q: $q,
    CSRF: CSRF,
    ProductRequiredSignoffs: ProductRequiredSignoffs,
    PermissionsRequiredSignoffs: PermissionsRequiredSignoffs,
    required_signoffs: required_signoffs,
  });
});
