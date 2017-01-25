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

    var required_signoffs = {};

    // Collect all of the new roles and signoff requirements
    $("#new_roles").find("tr").each(function(index, rs) {
      rs = $(rs);
      var role = rs.find("input[name='role']")[0].value;
      var signoffs_required = rs.find("input[name='signoffs_required']")[0].value;
      if (role in required_signoffs) {
        $scope.errors["role"] = "Cannot specify any Role more than once.";
      }
      else {
        required_signoffs[role] = signoffs_required;
      }
    });

    console.log($scope.errors);
    console.log(required_signoffs);

    if (Object.keys($scope.errors).length === 0) {
      CSRF.getToken()
      .then(function(csrf_token) {
        var service = null;
        var first = true;

        if ($scope.mode === "channel") {
          service = ProductRequiredSignoffs;
        }
        else if ($scope.mode === "permissions") {
          service = PermissionsRequiredSignoffs;
        }
        else {
          $scope.errors["exception"] = "Couldn't detect mode";
          $scope.saving = false;
        }

        var successCallback = function(response) {
          // TODO
        };
        var errorCallback = function(response, status) {
          // TODO
        };

        for (var role in required_signoffs) {
          var data = {"product": $scope.product, "role": role, "signoffs_required": required_signoffs[role], "csrf_token": csrf_token};
          if ($scope.mode === "channel") {
            data["channel"] = $scope.channel;
          }
          if (first) {
            first = false;

            service.addRequiredSignoff(data)
            .success(successCallback)
            .error(errorCallback);
          }
          else {
            // todo: add rs stuff to data
            service.addScheduledChange(data)
            .success(successCallback)
            .error(errorCallback);
          }
        }
      });
    }
    // todo: this probably isn't getting set in exception cases
    $scope.saving = false;
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
