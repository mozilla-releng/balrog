angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, $q, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Permissions) {
  $scope.loading = true;

  $scope.current_required_signoffs = {};
  $scope.pending_required_signoffs = {};
  $scope.all_products = [];
  $scope.selected_product = null;
  $scope.state = "current";
  $scope.current_user = null;
  $scope.user_roles = [];

  $scope.isEmpty = function(obj) {
    if (Object.keys(obj).length === 0) {
      return true;
    }
    return false;
  };

  var loading_deferreds = {
    "product": $q.defer(),
    "permissions": $q.defer(),
    "product_sc": $q.defer(),
    "permissions_sc": $q.defer(),
    "current_user": $q.defer(),
  };

  $q.all([loading_deferreds["product"].promise, loading_deferreds["permissions"].promise,
          loading_deferreds["product_sc"].promise, loading_deferreds["permissions_sc"].promise])
  .then(function() {
    $scope.loading = false;
  });

  var update_products = function(obj) {
    obj.forEach(function(product) {
      if (! $scope.all_products.includes(product)) {
        $scope.all_products.push(product);
      }
    });
  }
  $scope.$watch("current_required_signoffs", function() {
    update_products($scope.current_required_signoffs);
  }, true);
  $scope.$watch("pending_required_signoffs", function() {
    update_products($scope.pending_required_signoffs);
  }, true);

  ProductRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.current_required_signoffs)) {
          $scope.current_required_signoffs[rs.product] = {};
        }
    
        if (! ("channels" in $scope.current_required_signoffs[rs.product])) {
          $scope.current_required_signoffs[rs.product]["channels"] = {};
        }
    
        if (! (rs.channel in $scope.current_required_signoffs[rs.product]["channels"])) {
          $scope.current_required_signoffs[rs.product]["channels"][rs.channel] = {};
        }
    
        $scope.current_required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
          "required_signoffs": {},
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": null,
          "scheduled_by": null,
          "sc_data_version": null,
          "signoffs": {},
          "change_type": null,
        };
      });
    }
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load Product Required Signoffs:",
      response
    );
  })
  .finally(function() {
    loading_deferreds["product"].resolve();
  });

  PermissionsRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.current_required_signoffs)) {
          $scope.current_required_signoffs[rs.product] = {};
        }

        if (! ("permissions" in $scope.current_required_signoffs[rs.product])) {
          $scope.current_required_signoffs[rs.product]["permissions"] = {};
        }

        $scope.current_required_signoffs[rs.product]["permissions"][rs.role] = {
          "required_signoffs": {},
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "scheduled_by": null,
          "sc_id": null,
          "sc_data_version": null,
          "signoffs": {},
          "change_type": null,
        };
      });
    }
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load Permissions Required Signoffs:",
      response
    );
  })
  .finally(function() {
    loading_deferreds["permissions"].resolve();
  });

  ProductRequiredSignoffs.getScheduledChanges()
  .success(function(response) {
    if (response["count"] > 0) {
      response["scheduled_changes"].forEach(function(rs) {
        if (! (rs.product in $scope.pending_required_signoffs)) {
          $scope.pending_required_signoffs[rs.product] = {};
        }

        if (! ("channels" in $scope.pending_required_signoffs[rs.product])) {
          $scope.pending_required_signoffs[rs.product]["channels"] = {};
        }
    
        if (! (rs.channel in $scope.pending_required_signoffs[rs.product]["channels"])) {
          $scope.pending_required_signoffs[rs.product]["channels"][rs.channel] = {};
        }

        $scope.pending_required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
          "required_signoffs": rs.required_signoffs,
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": rs.sc_id,
          "scheduled_by": rs.scheduled_by,
          "sc_data_version": rs.sc_data_version,
          "signoffs": rs.signoffs,
          "change_type": rs.change_type,
        };
      });
    }
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load pending Product Required Signoffs:",
      response
    );
  })
  .finally(function() {
    loading_deferreds["product_sc"].resolve();
  });

  PermissionsRequiredSignoffs.getScheduledChanges()
  .success(function(response) {
    if (response["count"] > 0) {
      response["scheduled_changes"].forEach(function(rs) {
        if (! (rs.product in $scope.pending_required_signoffs)) {
          $scope.pending_required_signoffs[rs.product] = {};
        }

        if (! ("permissions" in $scope.pending_required_signoffs[rs.product])) {
          $scope.pending_required_signoffs[rs.product]["permissions"] = {};
        }
    
        $scope.pending_required_signoffs[rs.product]["permissions"][rs.role] = {
          "required_signoffs": rs.required_signoffs,
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": rs.sc_id,
          "scheduled_by": rs.scheduled_by,
          "sc_data_version": rs.sc_data_version,
          "signoffs": rs.signoffs,
          "change_type": rs.change_type,
        };
      });
    }
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load pending Permissions Required Signoffs:",
      response
    );
  })
  .finally(function() {
    loading_deferreds["permissions_sc"].resolve();
  });

  Permissions.getCurrentUser()
  .success(function(response) {
    $scope.current_user = response["username"];
    $scope.user_roles = Object.keys(response["roles"]);
  })
  .error(function(response) {
    sweetAlert(
      "Failed to load current user Roles:",
      response
    );
  })
  .finally(function() {
    loading_deferreds["current_user"].resolve();
  });


  $scope.addNewRequiredSignoff = function() {
    $modal.open({
      templateUrl: "required_signoff_modal.html",
      controller: "NewRequiredSignoffCtrl",
      backdrop: "static",
      resolve: {
        current_required_signoffs: function() {
          return $scope.current_required_signoffs;
        },
        pending_required_signoffs: function() {
          return $scope.pending_required_signoffs;
        },
      }
    });
  };

  $scope.editRequiredSignoffs = function(mode, channel = "") {
    $modal.open({
      templateUrl: "required_signoff_modal.html",
      controller: "EditRequiredSignoffsCtrl",
      backdrop: "static",
      resolve: {
        mode: function() {
          return mode;
        },
        channel: function() {
          return channel;
        },
        product: function() {
          return $scope.selected_product;
        },
        current_required_signoffs: function() {
          return $scope.current_required_signoffs;
        },
        pending_required_signoffs: function() {
          return $scope.pending_required_signoffs;
        },
      }
    });
  };

  $scope.deleteRequiredSignoffs = function(mode, channel = "") {
    $modal.open({
      templateUrl: "required_signoff_delete_modal.html",
      controller: "DeleteRequiredSignoffsCtrl",
      backdrop: "static",
      resolve: {
        current_required_signoffs: function() {
          return current_required_signoffs;
        },
        pending_required_signoffs: function() {
          return pending_required_signoffs;
        },
        mode: function() {
          return mode;
        },
        product: function() {
          return $scope.selected_product;
        },
        channel: function() {
          return channel;
        },
      }
    });
  };

  $scope.signoff = function(mode, sc_id, role, details, channel = "") {
    // need to bail if user has already signed off
    $modal.open({
      templateUrl: "signoff_modal.html",
      controller: "SignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Required Signoff";
        },
        service: function() {
          if (mode === "channel") {
            return ProductRequiredSignoffs;
          }
          else if (mode === "permission") {
            return PermissionsRequiredSignoffs;
          }
        },
        current_user: function() {
          return $scope.current_user;
        },
        user_roles: function() {
          return $scope.user_roles;
        },
        sc_id: function() {
          return sc_id;
        },
        pk: function() {
          pk = {"product": $scope.selected_product, "role": role};
          if (mode === "channel") {
            pk["channel"] = channel;
          }
          return pk;
        },
        data: function() {
          return {"signoffs_required": details["signoffs_required"]};
        },
        details: function() {
          // maybe should filter this ?
          return details;
        },
      }
    });
  };

  $scope.revokeSignoff = function(mode, sc_id, role, details, channel = "") {
    $modal.open({
      templateUrl: "revoke_signoff_modal.html",
      controller: "RevokeSignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Required Signoff";
        },
        service: function() {
          if (mode === "channel") {
            return ProductRequiredSignoffs;
          }
          else if (mode === "permission") {
            return PermissionsRequiredSignoffs;
          }
        },
        current_user: function() {
          return $scope.current_user;
        },
        sc_id: function() {
          return sc_id;
        },
        pk: function() {
          pk = {"product": $scope.selected_product, "role": role};
          if (mode === "channel") {
            pk["channel"] = channel;
          }
          return pk;
        },
        data: function() {
          return {"signoffs_required": details["signoffs_required"]};
        },
        details: function() {
          // maybe should filter this ?
          return details;
        },
      }
    });
  };
});
