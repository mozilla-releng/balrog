angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, $q, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.loading = true;

  $scope.current_required_signoffs = {};
  $scope.pending_required_signoffs = {};
  $scope.required_signoffs = {};
  $scope.selected_product = null;
  $scope.state = "current";

  var loading_deferreds = {
    "product": $q.defer(),
    "permissions": $q.defer(),
    "product_sc": $q.defer(),
    "permissions_sc": $q.defer(),
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

  $scope.$watch("state", function () {
    if ($scope.state === "current") {
      $scope.required_signoffs = $scope.current_required_signoffs;
    }
    else {
      $scope.required_signoffs = $scope.pending_required_signoffs;
    }
  });

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
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
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

        else if (! ("permissions" in $scope.current_required_signoffs[rs.product])) {
          $scope.current_required_signoffs[rs.product]["permissions"] = {};
        }
      
        $scope.current_required_signoffs[rs.product]["permissions"][rs.role] = {
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
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
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": rs.sc_id,
          "sc_data_version": rs.sc_data_version,
          "signoffs": rs.signoffs,
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
    
        else if (! ("permissions" in $scope.pending_required_signoffs[rs.product])) {
          $scope.pending_required_signoffs[rs.product]["permissions"] = {};
        }
      
        $scope.pending_required_signoffs[rs.product]["permissions"][rs.role] = {
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
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

  $scope.signoff = function(mode, sc_id) {
    // need to bail if user has already signed off
    $modal.open({
      templateUrl: "signoff_modal.html",
      controller: "SignoffCtrl",
      backdrop: "static",
      resolve: {
      }
    });
  };

  $scope.revokeSignoff = function(mode, sc_id) {
    $modal.open({
      templateUrl: "revoke_signoff_modal.html",
      controller: "RevokeSignoffCtrl",
      backdrop: "static",
      resolve: {
      }
    });
  };
});
