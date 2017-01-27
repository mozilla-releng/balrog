angular.module("app").controller("EditRequiredSignoffsCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, product, channel, required_signoffs, mode) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = mode;
  $scope.product = product;
  $scope.channel = channel;

  $scope.getTitle = function () {
    var title = "Signoff Requirements";
    if ($scope.product !== "") {
      if ($scope.mode === "channel" && $scope.channel !== "") {
        title += " for the " + $scope.product + " " + $scope.channel + " channel";
      }
      else if ($scope.mode === "permissions") {
        title += " for " + $scope.product + " Permissions";
      }
    }
    return title;
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
