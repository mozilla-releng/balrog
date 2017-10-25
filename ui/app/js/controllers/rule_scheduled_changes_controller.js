angular.module("app").controller("RuleScheduledChangesController",
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route, Releases, Permissions, Page, ProductRequiredSignoffs) {

  Page.setTitle('Scheduled Rule Changes');

  $scope.loading = true;
  $scope.failed = false;
  $scope.current_user = null;
  $scope.user_roles = [];

  $scope.sc_id = parseInt($routeParams.sc_id, 10);

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
  });

  ProductRequiredSignoffs.getRequiredSignoffs()
    .then(function(payload) {
      $scope.signoffRequirements = payload.data.required_signoffs;
    });

  function loadPage(newPage) {
    Rules.getScheduledChangeHistory($scope.sc_id, $scope.pageSize, newPage)
    .success(function(response) {
      $scope.scheduled_changes = response.revisions;
      $scope.scheduled_changes_rules_count = response.count;
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  if ($scope.sc_id) {
    // history of a specific rule
    $scope.$watch("currentPage", function(newPage) {
      loadPage(newPage);
    });
  } else {
  Rules.getScheduledChanges()
  .success(function(response) {
    // "when" is a unix timestamp, but it's much easier to work with Date objects,
    // so we convert it to that before rendering.
    $scope.scheduled_changes = response.scheduled_changes.map(function(sc) {
      if (sc.when !== null) {
        sc.when = new Date(sc.when);
      }
      return sc;
    });
  })
  .error(function() {
    console.error(arguments);
    $scope.failed = true;
  })
  .finally(function() {
    $scope.loading = false;
  });
  }

  $scope.$watch("ordering_str", function(value) {
    $scope.ordering = value.value.split(",");
  });


   if ($scope.sc_id) {
    $scope.ordering_options = [
      {
        text: "Data Version",
        value: "-data_version"
      },
    ];
  } else {
    $scope.ordering_options = [
    {
      text: "When",
      value: "when"
    },
    {
      text: "Product, Channel",
      value: "product,channel"
    },
  ];
  }

  $scope.ordering_str = $scope.ordering_options[0];

  $scope.currentPage = 1;
  $scope.pageSize = 10;

  $scope.state_filter = [
    {
      text: "Active",
      value: "active",
    },
    {
      text: "Completed",
      value: "complete",
    },
  ];
  $scope.state_str = $scope.state_filter[0];

  $scope.filterBySelect = function(sc) {
    if($scope.sc_id) {
      return true;
    }
    if ($scope.state_str.value === "complete" && sc.complete) {
      return true;
    }
    else if ($scope.state_str.value === "active" && !sc.complete) {
      return true;
    }
    return false;
  };

  $scope.openNewScheduledRuleChangeModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'rule_scheduled_change_modal.html',
      controller: 'NewRuleScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return $scope.scheduled_changes;
        },
        original_row: function() {
          return {};
        },
        sc: function() {
          // blank new default rule
          return {
            product: '',
            backgroundRate: 0,
            priority: 0,
            update_type: 'minor',
            when: null,
            change_type: 'insert',
          };
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
      }
    });
  };

  $scope.signoff = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "signoff_modal.html",
      controller: "SignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Rule";
        },
        service: function() {
          return Rules;
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
          return {"rule_id": sc["rule_id"]};
        },
        // todo: add more stuff here
        data: function() {
          return {
            "product": sc["product"],
            "channel": sc["channel"],
            "priority": sc["priority"],
            "backgroundRate": sc["backgroundRate"],
            "version": sc["version"],
          };
        },
      }
    });
  };

  $scope.revokeSignoff = function(sc) {
    $modal.open({
      templateUrl: "revoke_signoff_modal.html",
      controller: "RevokeSignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Rule";
        },
        service: function() {
          return Rules;
        },
        current_user: function() {
          return $scope.current_user;
        },
        sc: function() {
          return sc;
        },
        pk: function() {
          // TODO: add alias here if it exists
          return {"rule_id": sc["rule_id"]};
        },
        data: function() {
          return {
            "product": sc["product"],
            "channel": sc["channel"],
            "priority": sc["priority"],
            "backgroundRate": sc["backgroundRate"],
            "version": sc["version"],
          };
        },
      }
    });
  };

  $scope.openUpdateModal = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "rule_scheduled_change_modal.html",
      controller: "EditRuleScheduledChangeCtrl",
      size: 'lg',
      backdrop: 'static',
      resolve: {
        sc: function() {
          sc.when = new Date(sc.when);
          return sc;
        },
        original_row: function() {
          return {};
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
      }
    });
  };

  $scope.openDeleteModal = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "rule_scheduled_change_delete_modal.html",
      controller: "DeleteRuleScheduledChangeCtrl",
      backdrop: 'static',
      resolve: {
        sc: function() {
          return sc;
        },
        scheduled_changes: function() {
          return $scope.scheduled_changes;
        }
      }
    });
  };

  $scope.openReleaseDataModal = function(mapping) {
    Releases.getRelease(mapping)
    .success(function(response) {
      // it's the same rule, but this works
      var modalInstance = $modal.open({
        templateUrl: 'release_data_modal.html',
        controller: 'ReleaseDataCtrl',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          release: function () {
            return response;
          },
          diff: function() {
            return false;
          }
        }
      });
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  };
});
