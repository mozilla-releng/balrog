angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, Permissions, Page) {

  Page.setTitle('Signoffs');

  $scope.loading = true;

  // required_signoffs holds ALL of the Required Signoffs - product, permissions,
  // and scheduled changes for each. In an ideal world, this should probably be
  // an object with a bunch of setters and getters. As things stand now, there's
  // lots of repeated code because of the "if not exists" checks that need to
  // happen at each level of it.
  $scope.required_signoffs = {};
  $scope.selected_product = null;
  $scope.state = "current";
  $scope.current_user = localStorage.getItem("username");
  $scope.user_roles = [];

  // All of the initial loads happen asynchronously. We keep track of these so we can
  // set $scope.loading properly when they're all done.
  var loading_deferreds = {
    "product": $q.defer(),
    "permissions": $q.defer(),
    "product_sc": $q.defer(),
    "permissions_sc": $q.defer(),
    "user_info": $q.defer(),
  };

  $q.all([loading_deferreds["product"].promise, loading_deferreds["permissions"].promise,
          loading_deferreds["product_sc"].promise, loading_deferreds["permissions_sc"].promise])
  .then(function() {
    $scope.loading = false;
  });

  // The drop down that relies on this is only empty when there's absolutely no Required Signoffs
  // in the database, so this is mostly unused...
  $scope.$watch("required_signoffs", function() {
    if ($scope.selected_product === null) {
      var products = Object.keys($scope.required_signoffs);
      if (products.length > 0) {
        $scope.selected_product = products[0];
      }
    }
  }, true);

  $scope.undoRemoveRole = function(roleName, rs) {
    var product = Object.keys(rs)[0];
    var channel = Object.keys(rs[product].channels)[0];

    CSRF.getToken()
    .then(function(csrf_token) {
      var sc_id = $scope.required_signoffs[product].channels[channel][roleName].sc.sc_id;
      var data = {
        "csrf_token": csrf_token,
        "sc_data_version": $scope.required_signoffs[product].channels[channel][roleName].sc.sc_data_version
      };
      ProductRequiredSignoffs.deleteScheduledChange(sc_id, data)
      .success(function(response) {
        $scope.required_signoffs[product].channels[channel][roleName].sc = null;
      });
    });

  };

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
        };

        if (! ("sc" in $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role]["sc"] = null;
        }
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
        };

        if (! ("sc" in $scope.required_signoffs[rs.product]["permissions"][rs.role])) {
          $scope.required_signoffs[rs.product]["permissions"][rs.role]["sc"] = null;
        }
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

        if (! (rs.role in $scope.required_signoffs[rs.product]["channels"][rs.channel])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
            "signoffs_required": 0,
            "data_version": null,
          };
        }

        $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role]["sc"] = {
          "required_signoffs": rs.required_signoffs,
          "signoffs_required": rs.signoffs_required || 0,
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

        if (! (rs.role in $scope.required_signoffs[rs.product]["permissions"])) {
          $scope.required_signoffs[rs.product]["permissions"][rs.role] = {
            "signoffs_required": 0,
            "data_version": null,
          };
        }

        $scope.required_signoffs[rs.product]["permissions"][rs.role]["sc"] = {
          "required_signoffs": rs.required_signoffs,
          "signoffs_required": rs.signoffs_required || 0,
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

  Permissions.getUserInfo($scope.current_user)
  .then(function(response) {
    $scope.user_roles = Object.keys(response["roles"]);
    loading_deferreds["user_info"].resolve();
  },
  function(response) {
    sweetAlert(
      "Failed to load current user Roles:",
      response
    );
    loading_deferreds["user_info"].resolve();
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
        current_user: function() {
          return $scope.current_user;
        },
      }
    });
  };

  $scope.editRequiredSignoffs = function(mode, channel) {
    channel = channel || "";
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
        current_user: function() {
          return $scope.current_user;
        },
      }
    });
  };

  $scope.deleteRequiredSignoffs = function(required_signoffs, mode, channel) {
    channel = channel || "";
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
        current_user: function() {
          return $scope.current_user;
        },
      }
    });
  };

  $scope.signoff = function(mode, sc, role, channel) {
    channel = channel || "";
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
        required_signoffs: function () {
          return sc["required_signoffs"];
        },
        sc: function() {
          return sc;
        },
        pk: function() {
          pk = {"product": $scope.selected_product, "role": role};
          if (mode === "channel") {
            pk["channel"] = channel;
          }
          return pk;
        },
        data: function() {
          return {"signoffs_required": sc["signoffs_required"]};
        },
      }
    });
  };

  $scope.revokeSignoff = function(mode, sc, role, channel) {
    channel = channel || "";
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
        sc: function() {
          return sc;
        },
        pk: function() {
          pk = {"product": $scope.selected_product, "role": role};
          if (mode === "channel") {
            pk["channel"] = channel;
          }
          return pk;
        },
        data: function() {
          return {"signoffs_required": sc["signoffs_required"]};
        },
      }
    });
  };
});
