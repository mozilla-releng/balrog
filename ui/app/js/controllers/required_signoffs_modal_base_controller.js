angular.module("app").controller("BaseRequiredSignoffCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Rules,
         required_signoffs, mode, product, channel, current_roles, editing) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = mode;
  $scope.product = product;
  $scope.channel = channel;
  // When saveChanges is called, new_roles contains whatever the user has entered.
  // We need the original version as well, so we can compare the two and figure
  // out how to move from the current state to the new state.
  $scope.new_roles = $.extend(true, [], current_roles);
  $scope.editing = editing;

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
    $scope.new_roles.push({"role": "", "signoffs_required": null, "sc_id": null});
  };

  $scope.removeRole = function(index) {
    $scope.new_roles.splice(index, 1);
  };

  $scope.saveChanges = function() {
    $scope.errors = {};

    if (Object.keys($scope.new_roles).length === 0) {
      $scope.errors["exception"] = "No roles found!";
      return;
    }

    if ($scope.mode === "channel") {
      service = ProductRequiredSignoffs;
    }
    else if ($scope.mode === "permissions") {
      service = PermissionsRequiredSignoffs;
    }
    else {
      $scope.errors["exception"] = "Couldn't detect mode";
      return;
    }

    $scope.saving = true;
    console.log(current_roles);
    console.log($scope.new_roles);
    CSRF.getToken()
    .then(function(csrf_token) {
      var promises = [];
      var first = true;

      var current_role_names = [];
      var new_role_names = [];
      var all_role_names = [];
      current_roles.forEach(function(rs) {
        if (rs["role"] !== "") {
          current_role_names.push(rs["role"]);
          all_role_names.push(rs["role"]);
        }
      });
      $scope.new_roles.forEach(function(rs) {
        if (rs["role"] !== "") {
          new_role_names.push(rs["role"]);
          if (all_role_names.indexOf(rs["role"]) === -1) {
            all_role_names.push(rs["role"]);
          }
        }
      });

      // TODO: create_sc needs to be false if a thing is already a scheduled change. we should only
      // create for things that aren't scheduled
      all_role_names.forEach(function(role_name) {
        // todo: probably handle this further down
        //var is_sc = new_rs["sc_id"] ? false : true;
        // The safe thing to do is default to creating a scheduled change.
        // This will get overridden below in the one case where we shouldn't.
        var create_sc = true;
        var action = null;
        var role = null;

        // todo: need to pull actual role detail sout of correct data structure
        // If the role is only in the new Roles, we'll need to create it.
        if (current_role_names.indexOf(role_name) === -1 && new_role_names.indexOf(role_name) !== -1) {
          action = "insert";
          // If we're creating a new role, and there was already at least one before, we must use an SC.
          if (current_role_names.length === 0 && first) {
            create_sc = false;
          }
          for (let r of $scope.new_roles) {
            if (r["role"] === role_name) {
              role = r;
              break;
            }
          }
        }
        // If the role is only in the current Roles, we'll be deleting it
        else if (current_role_names.indexOf(role_name) !== -1 && new_role_names.indexOf(role_name) === -1) {
          action = "delete";
          for (let r of current_roles) {
            if (r["role"] === role_name) {
              role = r;
              break;
            }
          }
        }
        else {
          action = "update";
          for (let r of $scope.new_roles) {
            if (r["role"] === role_name) {
              for (let r2 of current_roles) {
                if (r["role"] === r2["role"]) {
                  if (r["signoffs_required"] === r2["signoffs_required"]) {
                    console.log("No change to " + role_name + ", skipping...");
                    return; // exit forEach
                  }
                  else {
                    role = r;
                  }
                }
              }
            }
          }
        }

        first = false;
        console.log("Role: " + role_name);
        console.log("Action: " + action);
        console.log("Create SC: " + create_sc);
        console.log("object: ");
        console.log(role);

        var successCallback = function(data, deferred) {
          return function(response) {
            var data_version = 1;
            // how do we know if this is for data_version or sc_data_version?
            if (response.hasOwnProperty("new_data_version")) {
              data_version = response["new_data_version"];
            }
            // need to set this to whatever is in new_roles for the role
            var sc_id = null;
            if (response.hasOwnProperty("sc_id")) {
              sc_id = response["sc_id"];
            }

            if (! (required_signoffs.hasOwnProperty(data["product"]))) {
              required_signoffs[data["product"]] = {"channels": {}, "permissions": {}};
            }
            var namespace = required_signoffs[data["product"]]["permissions"];
            if ($scope.mode === "channel") {
              if (! (required_signoffs[data["product"]]["channels"].hasOwnProperty(data["channel"]))) {
                required_signoffs[data["product"]]["channels"][data["channel"]] = {};
              }
              namespace = required_signoffs[data["product"]]["channels"][data["channel"]];
            }
            console.log(namespace);

            // need to remove rather than add for deletes
            namespace[data["role"]] = {
              "signoffs_required": data["signoffs_required"],
              // should this be sc_data_version? we can never update required signoffs directly, so maybe no point in storing
              // regular data_version?
              "data_version": data_version,
              "sc_id": sc_id,
            };

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

        var deferred = $q.defer();
        promises.push(deferred.promise);
        var data = {"product": $scope.product, "role": role_name, "signoffs_required": role["signoffs_required"], "csrf_token": csrf_token,
                    "data_version": role["data_version"], "sc_data_version": role["sc_data_version"]};
        if ($scope.mode === "channel") {
          data["channel"] = $scope.channel;
        }
        if (create_sc) {
          data["change_type"] = action;
          // There's no use case for users to pick a specific time for these
          // to be enacted, so we just schedule them for 5 seconds in the future.
          // They'll still end up waiting for any necessary Required Signoffs
          // before being enacted, however.
          data["when"] = new Date().getTime() + 5000;
          service.addScheduledChange(data)
          .success(successCallback(data, deferred))
          .error(errorCallback(data, deferred));
        }
        else if (role["sc_id"] !== null) {
          if (action === "delete") {
            service.deleteScheduledChange(role["sc_id"], data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
          else {
            service.updateScheduledChange(role["sc_id"], data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
        }
        else {
          if (action === "insert") {
            service.addRequiredSignoff(data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
          // updates and deletes aren't supported outside of scheduled changes
        }
      });

      $q.all(promises)
      .then(function() {
        if (Object.keys($scope.errors).length === 0) {
          $modalInstance.close();
        }
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
