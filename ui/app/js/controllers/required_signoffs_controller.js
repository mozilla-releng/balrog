angular.module("app").controller('RequiredSignoffsController',
function($scope, $modal, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.loading = true;

  $scope.current_required_signoffs = {};
  $scope.pending_required_signoffs = {};
  $scope.required_signoffs = {};
  $scope.selected_product = null;
  $scope.state = "current";

  // TODO: make work for pending
  $scope.$watch("current_required_signoffs", function() {
    if ($scope.selected_product === null) {
      var products = Object.keys($scope.current_required_signoffs);
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

  // Grabbing initial data from the server
  ProductRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.current_required_signoffs)) {
          $scope.current_required_signoffs[rs.product] = {"channels": {}};
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

    PermissionsRequiredSignoffs.getRequiredSignoffs()
    .success(function(response) {
      if (response["count"] > 0) {
        response["required_signoffs"].forEach(function(rs) {
          if (! (rs.product in $scope.current_required_signoffs)) {
            $scope.current_required_signoffs[rs.product] = {"permissions": {}};
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
    // can a response be grabbed here?
    .error(function(response) {
      alert("error! " + response);
    });
  })
  // can a response be grabbed here?
  .error(function(response) {
    alert("error! " + response);
  });

  ProductRequiredSignoffs.getScheduledChanges()
  .success(function(response) {
    if (response["count"] > 0) {
      response["scheduled_changes"].forEach(function(rs) {
        if (! (rs.product in $scope.pending_required_signoffs)) {
          $scope.pending_required_signoffs[rs.product] = {"channels": {}};
        }
    
        if (! (rs.channel in $scope.pending_required_signoffs[rs.product]["channels"])) {
          $scope.pending_required_signoffs[rs.product]["channels"][rs.channel] = {};
        }
    
        $scope.pending_required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
          "signoffs_required": rs.signoffs_required,
          "data_version": rs.data_version,
          "sc_id": rs.sc_id,
          "sc_data_version": rs.sc_data_version,
        };
      });
    }
  })
  // can a response be grabbed here?
  .error(function(response) {
    alert("error! " + response);
  })
  .finally(function() {
    // todo: probably should use $q and defer until all loads are done.
    $scope.loading = false;
  });

  // Setting up dialogs the page uses
  $scope.addNewRequiredSignoff = function() {
    $modal.open({
      templateUrl: "required_signoff_modal.html",
      controller: "NewRequiredSignoffCtrl",
      backdrop: "static",
      resolve: {
        required_signoffs: function() {
          return $scope.current_required_signoffs;
        },
      }
    });
  };

  $scope.editRequiredSignoffs = function(required_signoffs, mode, channel = "") {
    $modal.open({
      templateUrl: "required_signoff_modal.html",
      controller: "EditRequiredSignoffsCtrl",
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
});
