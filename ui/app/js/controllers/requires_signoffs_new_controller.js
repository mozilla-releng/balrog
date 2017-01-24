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

  $scope.saveChanges = function() {
    $scope.saving = true;
    $scope.errors = {};

    var roles = {};

    // collect all of the new roles and signoff requirements
    $("#new_roles").find("tr").each(function(index, rs) {
    //for (var rs in $("#new_roles").find("tr")) {
      rs = $(rs);
      console.log(rs.find("input[name='role']")[0].value);
      console.log(rs.find("input[name='signoffs_required']")[0].value);
    });

    CSRF.getToken()
    .then(function(csrf_token) {
      for (var i = 0; i < $scope.new_roles; i++) {
        if ($scope.mode === "channel") {
          if (i === 0) {
          }
        }
        else if ($scope.mode === "permissions") {
        }
      }
    });
    $scope.saving = false;
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
