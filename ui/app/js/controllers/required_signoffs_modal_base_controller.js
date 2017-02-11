angular.module("app").controller("BaseRequiredSignoffCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Rules,
         required_signoffs, mode, product, channel, current_user, current_roles, editing) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = mode;
  $scope.product = product;
  $scope.channel = channel;
  // When saveChanges is called, new_roles contains whatever the user has entered.
  // We need the original version as well, so we can compare the two and figure
  // out how to move from the current state to the new state.
  $scope.new_roles = $.extend(true, [], current_roles);
  $scope.current_roles = current_roles;
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
    $scope.new_roles.push({"role": "", "signoffs_required": null, "sc": null});
  };

  $scope.removeRole = function(index) {
    $scope.new_roles.splice(index, 1);
  };

  $scope.saveChanges = function() {
    $scope.errors = {};
    var service = null;

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
    CSRF.getToken()
    .then(function(csrf_token) {
      var deferreds = {};
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

      all_role_names.forEach(function(role_name) {
        // The safe thing to do is to assume signoff is required.
        // This will get overridden below in the one case where we shouldn't.
        var requires_signoff = true;
        var action = null;
        var pending = false;
        var role = null;

        // If the role is only in the new Roles, we'll need to create it.
        if (current_role_names.indexOf(role_name) === -1 && new_role_names.indexOf(role_name) !== -1) {
          action = "insert";
          // If we're creating a new role, and there wasn't any already, signoff won't be required
          if (current_role_names.length === 0 && first) {
            requires_signoff = false;
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
              pending = r["sc"] ? true : false;
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
                  if (r["sc"]) {
                    pending = true;
                    role = r;
                    if (r["sc"]["signoffs_required"] === r2["sc"]["signoffs_required"]) {
                      console.log("No change to " + role_name + ", skipping...");
                      return; // exit forEach
                    }
                  }
                  else {
                    role = r;
                    if (r["signoffs_required"] === r2["signoffs_required"]) {
                      console.log("No change to " + role_name + ", skipping...");
                      return; // exit forEach
                    }
                  }
                }
              }
            }
          }
        }

        first = false;

        var addScheduledChangeCallback = function(data, deferred) {
          return function(response) {
            if ($scope.mode === "channel") {
              if (data["change_type"] === "insert") {
                // this may not work if the first direct add doesn't happen first.
                required_signoffs[$scope.product]["channels"][$scope.channel][data["role"]] = {
                  "signoffs_required": 0,
                  "data_version": null,
                  "sc": {
                    // how to set required signoffs correctly? backend doesn't return it
                    "required_signoffs": {},
                    "signoffs_required": data["signoffs_required"] || 0,
                    "sc_id": response["sc_id"],
                    "scheduled_by": current_user,
                    "sc_data_version": 1,
                    "signoffs": {},
                    "change_type": data["change_type"],
                  },
                };
              }
              else {
                required_signoffs[$scope.product]["channels"][$scope.channel][data["role"]]["sc"] = {
                  // how to set required signoffs correctly? backend doesn't return it
                  "required_signoffs": {},
                  "signoffs_required": data["signoffs_required"] || 0,
                  "sc_id": response["sc_id"],
                  "scheduled_by": current_user,
                  "sc_data_version": 1,
                  "signoffs": {},
                  "change_type": data["change_type"],
                };
              }
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

        deferreds[role_name] = $q.defer();
        console.log(deferreds[role_name]);
        promises.push(deferreds[role_name].promise);
        var data = {"product": $scope.product, "role": role_name, "csrf_token": csrf_token, "data_version": role["data_version"]};
        if ($scope.mode === "channel") {
          data["channel"] = $scope.channel;
        }

        // If there's no signoffs required yet, we can just create it directly!
        if (! requires_signoff) {
          data["signoffs_required"] = role["signoffs_required"];
          if (action === "insert") {
            service.addRequiredSignoff(data)
            .success(function(response) {
              if ($scope.mode === "channel") {
                if (! ($scope.product in required_signoffs)) {
                  required_signoffs[$scope.product] = {"channels": {}};
                }
                required_signoffs[$scope.product]["channels"][$scope.channel] = {};
                required_signoffs[$scope.product]["channels"][$scope.channel][role_name] = {
                    "signoffs_required": role["signoffs_required"],
                    "data_version": response["new_data_version"],
                    "sc": null,
                };
              }
              else {
                required_signoffs[$scope.product] = {"permissions": {}};
                required_signoffs[$scope.product]["permissions"][role_name] = {
                    "signoffs_required": role["signoffs_required"],
                    "data_version": response["new_data_version"],
                    "sc": null,
                };
              }
              deferreds[role_name].resolve();
            })
            .error(errorCallback(data, deferreds[role_name]));
          }
        }
        // Otherwise, we need to use Scheduled Changes
        else {
          // There's no use case for users to pick a specific time for these
          // to be enacted, so we just schedule them for 5 seconds in the future.
          // They'll still end up waiting for any necessary Required Signoffs
          // before being enacted, however.
          data["when"] = new Date().getTime() + 5000;
          // If we're working with an already pending change we just need to
          // update or delete it.
          if (pending) {
            data["sc_data_version"] = role["sc"]["sc_data_version"];
            if (action === "delete") {
              service.deleteScheduledChange(role["sc"]["sc_id"], data)
              .success(function(response) {
                if ($scope.mode === "channel") {
                  delete required_signoffs[$scope.product]["channels"][$scope.channel][role_name];
                }
                else {
                  delete required_signoffs[$scope.product]["permissions"][role_name];
                }
                deferreds[role_name].resolve();
              })
              .error(errorCallback(data, deferreds[role_name]));
            }
            else {
              data["signoffs_required"] = role["sc"]["signoffs_required"];
              service.updateScheduledChange(role["sc"]["sc_id"], data)
              .success(function(response) {
                if ($scope.mode === "channel") {
                  required_signoffs[$scope.product]["channels"][$scope.channel][role_name]["sc"]["signoffs_required"] = role["sc"]["signoffs_required"];
                }
                else {
                  required_signoffs[$scope.product]["permissions"][role_name]["sc"]["signoffs_required"] = role["sc"]["signoffs_required"];
                }
                deferreds[role_name].resolve();
              })
              .error(errorCallback(data, deferreds[role_name]));
            }
          }
          // Otherwise, we'll create a new Scheduled Change.
          else {
            data["change_type"] = action;
            if (action !== "delete") {
              data["signoffs_required"] = role["signoffs_required"];
            }
            service.addScheduledChange(data)
            // probably need to pass deferreds[role_name], not the .deferred?
            .success(addScheduledChangeCallback(data, deferreds[role_name]))
            .error(errorCallback(data, deferreds[role_name]));
          }
        }
      });

      console.log(promises);
      // this doesn't seem to be working. maybe the promises array isn't filled up yet, beacuse the above forEach is async?
      // maybe a two stage deferred will help....dunno
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
