angular.module("app").controller("BaseRequiredSignoffCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Rules,
         required_signoffs, mode, product, channel, editing) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = mode;
  $scope.product = product;
  $scope.channel = channel;
  $scope.new_roles = [];
  $scope.editing = editing;

  if ($scope.editing) {
    if ($scope.mode === "channel") {
      for (let role of Object.keys(required_signoffs[product]["channels"][channel])) {
        $scope.new_roles.push({
          "role": role,
          "signoffs_required": required_signoffs[product]["channels"][channel][role]["signoffs_required"],
          "sc_id": required_signoffs[product]["channels"][channel][role]["sc_id"],
        });
      }
    }
    else if ($scope.mode === "permissions") {
      for (let role of Object.keys(required_signoffs[product]["permissions"])) {
        $scope.new_roles.push({
          "role": role,
          "signoffs_required": required_signoffs[product]["permissions"][role]["signoffs_required"],
          "sc_id": required_signoffs[product]["permissions"][role]["sc_id"],
        });
      }
    }
  }
  else {
    $scope.new_roles = [{"role": "", "signoffs_required": null, "sc_id": null}];
  } 

  $scope.products = [];
  Rules.getProducts().success(function(response) {
    $scope.products = response.product;
  });
  $scope.channels = [];
  Rules.getChannels().success(function(response) {
    $scope.channels = response.channel;
  });

  $scope.length = function(item) {
    return item.length;
  };

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
    $scope.new_roles.push({"role": "", "signoffs_required": null});
  };

  $scope.removeRole = function(index) {
    $scope.new_roles.splice(index, 1);
  };

  $scope.saveChanges = function() {
    $scope.errors = {};

    var new_required_signoffs = {};

    for (let rs of $scope.new_roles) {
      if (rs["role"] !== "") {
        if (rs["role"] in new_required_signoffs) {
          $scope.errors["role"] = "Cannot specify any Role more than once.";
        }
        else {
          new_required_signoffs[rs["role"]] = rs["signoffs_required"];
        }
      }
    }

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
            var data_version = 1;
            var sc_id = null;
            if (response.hasOwnProperty("new_data_version")) {
              data_version = response["new_data_version"];
            }
            if (response.hasOwnProperty("sc_id")) {
              sc_id = response["sc_id"];
            }
            // todo: maybe required_signoffs should be an object with methods
            // so we don't have to duplicate this from the main controller
            if ($scope.mode === "channel") {
              if (! (data["product"] in required_signoffs)) {
                required_signoffs[data["product"]] = {"channels": {}};
              }

              if (! (data["channel"] in required_signoffs[data["product"]]["channels"])) {
                required_signoffs[data["product"]]["channels"][data["channel"]] = {};
              }
              required_signoffs[data["product"]]["channels"][data["channel"]][data["role"]] = {
                "signoffs_required": data["signoffs_required"],
                "data_version": data_version,
                "sc_id": sc_id,
              };
            }
            else if ($scope.mode === "permissions") {
              if (! (data["product"] in required_signoffs)) {
                required_signoffs[data["product"]] = {"permissions": {}};
              }
              else if (! ("permissions" in required_signoffs[data["product"]])) {
                required_signoffs[data["product"]]["permissions"] = {};
              }
          
              required_signoffs[data["product"]]["permissions"][data["role"]] = {
                "signoffs_required": data["signoffs_required"],
                "data_version": data_version,
                "sc_id": sc_id,
              };
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
