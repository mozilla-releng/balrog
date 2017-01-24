angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = "channel";
  $scope.product = "";
  $scope.channel = "";
  $scope.new_roles = 1;

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
  $scope.addRole = function() {
    $scope.new_roles++;
  };

  $scope.saveChanges = function() {
    $scope.saving = true;
    $scope.errors = {};

    CSRF.getToken()
    .then(function(csrf_token) {
    });
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
