angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, required_signoffs) {
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
    $scope.errors = {};

    var new_required_signoffs = {};

    // Collect all of the new roles and signoff requirements
    $("#new_roles > .new_role").each(function(index, rs) {
      rs = $(rs);
      var role = rs.find("input[name='role']")[0].value;
      var signoffs_required = rs.find("input[name='signoffs_required']")[0].value;
      if (role !== "") {
        if (role in new_required_signoffs) {
          $scope.errors["role"] = "Cannot specify any Role more than once.";
        }
        else {
          new_required_signoffs[role] = signoffs_required;
        }
      }
    });

    if (Object.keys(new_required_signoffs).length === 0) {
      $scope.errors["exception"] = "No new roles found!";
    }

    if (Object.keys($scope.errors).length === 0) {
      $scope.saving = true;

      CSRF.getToken()
      .then(function(csrf_token) {
        var service = null;
        var first = true;

        var promises = [];

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

        var successCallback = function(data, deferred) {
          return function(response) {
            // TODO: We need to change this so that Required Signoffs that are still
            // in a Scheduled state don't show up the same as others.
            var data_version = response["new_data_version"];
            // todo: maybe required_signoffs should be an object with methods
            // so we don't have to duplicate this from the main controller
            if (! (data["product"] in required_signoffs)) {
              required_signoffs[data["product"]] = {"channels": {}};
            }

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
            deferred.resolve();
          };
        };
        var errorCallback = function(data, deferred) {
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
            deferred.resolve();
          };
        };

        for (var role in new_required_signoffs) {
          var deferred = $q.defer();
          promises.push(deferred.promise);
          var data = {"product": $scope.product, "role": role, "signoffs_required": new_required_signoffs[role], "csrf_token": csrf_token};
          if ($scope.mode === "channel") {
            data["channel"] = $scope.channel;
          }
          if (first) {
            first = false;
            service.addRequiredSignoff(data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
          // There's probably a race condition here if this completes
          // before addRequiredSignoff from the first time through this loop.
          else {
            data["change_type"] = "insert";
            // There's no use case for users to pick a specific time for these
            // to be enacted, so we just schedule them for 30 seconds in the future.
            // They'll still end up waiting for any necessary Required Signoffs
            // before being enacted, however.
            data["when"] = new Date().getTime() + 30000;
            service.addScheduledChange(data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
        }

        $q.all(promises)
        .then(function() {
          if (Object.keys($scope.errors).length === 0) {
            $modalInstance.close();
          }
          $scope.saving = false;
        });
      });
    }
  };


  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
