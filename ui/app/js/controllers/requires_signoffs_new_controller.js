angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, required_signoffs) {
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

    var new_required_signoffs = {};

    // Collect all of the new roles and signoff requirements
    $("#new_roles > .new_role").find("tr").each(function(index, rs) {
      rs = $(rs);
      var role = rs.find("input[name='role']")[0].value;
      var signoffs_required = rs.find("input[name='signoffs_required']")[0].value;
      if (role in new_required_signoffs) {
        $scope.errors["role"] = "Cannot specify any Role more than once.";
      }
      else {
        new_required_signoffs[role] = signoffs_required;
      }
    });

    if (Object.keys(new_required_signoffs).length === 0) {
      $scope.errors["exception"] = "New new roles found!";
    }

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

        var successCallback = function(data) {
          return function(response) {
            var data_version = response["new_data_version"];
            // todo: maybe required_signoffs should be an object with methods
            // so we don't have to duplicate this from the main controller
            if (! (data["product"] in required_signoffs)) {
              required_signoffs[data["product"]] = {"channels": {}};
            }

            // TODO: this isn't updating the page properly. also need to close the modal
            if ($scope.mode === "channel") {
              if (! (data["channel"] in required_signoffs[data["product"]]["channels"])) {
                required_signoffs[data["product"]]["channels"][data["channel"]] = {};
              }
              required_signoffs[data["product"]]["channels"][data["channel"]][data["role"]] = {
                "signoffs_required": data["signoffs_required"],
                "data_version": data_version,
              };
            }
            else if ($scope.mode === "permissions") {
            }
          };
        };
        var errorCallback = function(data) {
          return function(response, status) {
            if (typeof response === "object") {
              $scope.errors = response;
            }
            else if (typeof response === "string"){
              $scope.errors["exception"] = response;
            }
            else {
              sweetAlert("Unknown error occurred");
            }
          };
        };

        for (var role in new_required_signoffs) {
          var data = {"product": $scope.product, "role": role, "signoffs_required": new_required_signoffs[role], "csrf_token": csrf_token};
          if ($scope.mode === "channel") {
            data["channel"] = $scope.channel;
          }
          if (first) {
            service.addRequiredSignoff(data)
            .success(successCallback(data))
            .error(errorCallback(data));
          }
          else {
            // todo: add rs stuff to data
            service.addScheduledChange(data)
            .success(successCallback(data))
            .error(errorCallback(data));
          }
        }
      });
    }
    // todo: this probably isn't getting set in exception cases
    if (Object.keys($scope.errors).length === 0) {
        $modalInstance.close();
    }
    $scope.saving = false;
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
