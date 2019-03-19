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
    $scope.new_roles.push({"name": "", "data_version": null, "signoffs_required": null, "sc": null, "new": true});
  };

  $scope.removeRole = function(index) {
    $scope.new_roles.splice(index, 1);
  };

  $scope.saveChanges = function() {
    $scope.errors = {};
    var service = null;
    var role_names = {
      "current": new Set(),
      "new": new Set(),
      "all": new Set(),
    };

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

    current_roles.forEach(function(role) {
      if (role["name"] !== "") {
        role_names["current"].add(role["name"]);
        role_names["all"].add(role["name"]);
      }
    });
    $scope.new_roles.forEach(function(role) {
      if (role["name"] !== "") {
        if (role_names["new"].has(role["name"])) {
          $scope.errors["exception"] = "Multiple entries found for " + role["name"] + ". Cannot continue.";
          return;
        }
        role_names["new"].add(role["name"]);
        role_names["all"].add(role["name"]);
      }
    });

    var get_role_changes = function(role_names, current_roles, new_roles) {
      var role_changes = [];
      var first_insert = true;

      role_names["all"].forEach(function(role_name) {
        var noop = false;
        var change = {
          "type": null,
          "pending": null,
          "role": null,
          "requires_signoff": true,
        };

        // If the role is only in the new Roles, we'll need to create it.
        if (! role_names["current"].has(role_name) && role_names["new"].has(role_name)) {
          change["type"] = "insert";
          change["role"] = new_roles.find(function(r) { return r["name"] === role_name; });
          change["pending"] = false;
          if (role_names["current"].size === 0 && first_insert) {
            change["requires_signoff"] = false;
            first_insert = false;
          }
        }
        // If the role is only in the current Roles, we'll be deleting it
        else if (role_names["current"].has(role_name) && ! role_names["new"].has(role_name)) {
          change["type"] = "delete";
          change["role"] = current_roles.find(function(r) { return r["name"] === role_name; });
          change["pending"] = change["role"]["sc"] ? true : false;
        }
        // Otherwise, it's an update
        else {
          var new_role = new_roles.find(function(r) { return r["name"] === role_name; });
          var current_role = current_roles.find(function(r) { return r["name"] === role_name; });

          change["type"] = "update";
          change["role"] = new_role;
          if (new_role["sc"]) {
            change["pending"] = true;
            if (new_role["sc"]["signoffs_required"] === current_role["sc"]["signoffs_required"]) {
              noop = true;
            }
          }
          else {
            change["pending"] = false;
            if (new_role["signoffs_required"] === current_role["signoffs_required"]) {
              noop = true;
            }
          }
        }

        if (! noop) {
          role_changes.push(change);
        }
      });
      return role_changes;
    };

    var process_role_changes = function(change, csrf_token) {
      return new Promise(function(resolve, reject) {
        var role_name = change["role"]["name"];
        var data = {"product": $scope.product, "role": role_name, "csrf_token": csrf_token, "data_version": change["role"]["data_version"]};
        if ($scope.mode === "channel") {
          data["channel"] = $scope.channel;
        }

        // If there's no signoffs required yet, we can just create it directly!
        if (! change["requires_signoff"]) {
          data["signoffs_required"] = change["role"]["signoffs_required"];
          if (change["type"] === "insert") {
            service.addRequiredSignoff(data)
            .success(function(response) {
              if ($scope.mode === "channel") {
                if (! ($scope.product in required_signoffs)) {
                  required_signoffs[$scope.product] = {"channels": {}};
                }
                if (! ("channels" in required_signoffs[$scope.product])) {
                  required_signoffs[$scope.product]["channels"] = {};
                }
                required_signoffs[$scope.product]["channels"][$scope.channel] = {};
                required_signoffs[$scope.product]["channels"][$scope.channel][role_name] = {
                    "signoffs_required": change["role"]["signoffs_required"],
                    "data_version": response["new_data_version"],
                    "sc": null,
                };
              }
              else {
                if (! ($scope.product in required_signoffs)) {
                  required_signoffs[$scope.product] = {"permissions": {}};
                }
                if (! ("permissions" in required_signoffs[$scope.product])) {
                  required_signoffs[$scope.product]["permissions"] = {};
                }
                required_signoffs[$scope.product]["permissions"][role_name] = {
                    "signoffs_required": change["role"]["signoffs_required"],
                    "data_version": response["new_data_version"],
                    "sc": null,
                };
              }
              resolve();
            })
            .error(reject);
          }
        }
        else {
          // There's no use case for users to pick a specific time for these
          // to be enacted, so we just schedule them for 5 seconds in the future.
          // They'll still end up waiting for any necessary Required Signoffs
          // before being enacted, however.
          data["when"] = new Date().getTime() + 5000;
          // If we're working with an already pending change we just need to
          // update or delete it.
          if (change["pending"]) {
            data["sc_data_version"] = change["role"]["sc"]["sc_data_version"];
            if (change["type"] === "delete") {
              service.deleteScheduledChange(change["role"]["sc"]["sc_id"], data)
              .success(function(response) {
                if ($scope.mode === "channel") {
                  // If there was _only_ a scheduled change, we can delete the entire Role.
                  if (required_signoffs[$scope.product]["channels"][$scope.channel][role_name]["data_version"] === null) {
                    delete required_signoffs[$scope.product]["channels"][$scope.channel][role_name];
                  }
                  // Otherwise, just reset the scheduled changes part
                  else {
                    required_signoffs[$scope.product]["channels"][$scope.channel][role_name]["sc"] = null;
                  }
                }
                else {
                  if (required_signoffs[$scope.product]["permissions"][role_name]["data_version"] === null) {
                    delete required_signoffs[$scope.product]["permissions"][role_name];
                  }
                  else {
                    required_signoffs[$scope.product]["permissions"][role_name]["sc"] = null;
                  }
                }
                resolve();
              })
              .error(reject);
            }
            else {
              data["signoffs_required"] = change["role"]["sc"]["signoffs_required"];
              service.updateScheduledChange(change["role"]["sc"]["sc_id"], data)
              .success(function(response) {
                if ($scope.mode === "channel") {
                  required_signoffs[$scope.product]["channels"][$scope.channel][role_name]["sc"]["sc_data_version"] = response["new_data_version"];
                  required_signoffs[$scope.product]["channels"][$scope.channel][role_name]["sc"]["signoffs_required"] = change["role"]["sc"]["signoffs_required"];
                }
                else {
                  required_signoffs[$scope.product]["permissions"][role_name]["sc"]["sc_data_version"] = response["new_data_version"];
                  required_signoffs[$scope.product]["permissions"][role_name]["sc"]["signoffs_required"] = change["role"]["sc"]["signoffs_required"];
                }
                resolve();
              })
              .error(reject);
            }
          }
          // Otherwise, we'll create a new Scheduled Change.
          else {
            data["change_type"] = change["type"];
            if (change["type"] !== "delete") {
              data["signoffs_required"] = change["role"]["signoffs_required"];
            }
            service.addScheduledChange(data)
            .success(function(response) {
              var sc = {
                // TODO: We should really be setting this, but the backend doesn't
                // return them.
                "required_signoffs": {},
                "signoffs_required": change["role"]["signoffs_required"] || 0,
                "sc_id": response["sc_id"],
                "scheduled_by": current_user,
                "sc_data_version": 1,
                "signoffs": {},
                "change_type": change["type"],
              };

              var roles = ($scope.mode === "channel") ?
                required_signoffs[$scope.product]["channels"][$scope.channel] :
                required_signoffs[$scope.product]["permissions"];

              if (data["change_type"] === "insert") {
                roles[role_name] = {
                  "signoffs_required": 0,
                  "data_version": null,
                };
              }
              roles[role_name]["sc"] = sc;
              resolve();
            })
            .error(reject);
          }
        }
      });
    };

    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      role_changes = get_role_changes(role_names, current_roles, $scope.new_roles);
      promises = role_changes.map(function(change) { return process_role_changes(change, csrf_token); });
      return $q.all(promises);
    })
    .then(function() {
      $scope.saving = false;
      $modalInstance.close();
    },
    function(response) {
      $scope.saving = false;
      if (typeof response === "object") {
        $scope.errors = response;
      }
      else if (typeof response === "string"){
        $scope.errors["exception"] = response;
      }
      else {
        sweetAlert("Unknown error occurred");
      }
    });
  };

  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
