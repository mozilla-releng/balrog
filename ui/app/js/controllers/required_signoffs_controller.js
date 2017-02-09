angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, $q, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Permissions) {
  $scope.loading = true;

  $scope.required_signoffs = {};
  $scope.selected_product = null;
  $scope.state = "current";
  $scope.current_user = null;
  $scope.user_roles = [];

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

  $scope.$watch("required_signoffs", function() {
    if ($scope.selected_product === null) {
      var products = Object.keys($scope.required_signoffs);
      if (products.length > 0) {
        $scope.selected_product = products[0];
      }
    }
  }, true);

  ProductRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {};
        }
    
        if (! ("channels" in $scope.required_signoffs[rs.product])) {
          $scope.required_signoffs[rs.product]["channels"] = {};
        }
    
        if (! (rs.channel in $scope.required_signoffs[rs.product]["channels"])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel] = {};
        }
    
        $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": null,
          "scheduled_by": null,
          "sc_data_version": null,
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
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {};
        }

        if (! ("permissions" in $scope.required_signoffs[rs.product])) {
          $scope.required_signoffs[rs.product]["permissions"] = {};
        }

        $scope.required_signoffs[rs.product]["permissions"][rs.role] = {
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "scheduled_by": null,
          "sc_id": null,
          "sc_data_version": null,
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
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {};
        }

        if (! ("channels" in $scope.required_signoffs[rs.product])) {
          $scope.required_signoffs[rs.product]["channels"] = {};
        }
    
        if (! (rs.channel in $scope.required_signoffs[rs.product]["channels"])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel] = {};
        }

        $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
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
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {};
        }

        if (! ("permissions" in $scope.required_signoffs[rs.product])) {
          $scope.required_signoffs[rs.product]["permissions"] = {};
        }
    
        $scope.required_signoffs[rs.product]["permissions"][rs.role] = {
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
        required_signoffs: function() {
          return $scope.required_signoffs;
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
        required_signoffs: function() {
          return $scope.required_signoffs;
        },
      }
    });
  };

  $scope.deleteRequiredSignoffs = function(required_signoffs, mode, channel = "") {
    $modal.open({
      templateUrl: "required_signoff_delete_modal.html",
      controller: "DeleteRequiredSignoffsCtrl",
      backdrop: "static",
      resolve: {
        required_signoffs: function() {
          return required_signoffs;
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
