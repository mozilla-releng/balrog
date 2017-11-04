angular.module("app").controller("PermissionScheduledChangesController",
function($scope, $routeParams, $location, $timeout, Permissions, Rules, Search, $modal, $route, Releases, Page,
         PermissionsRequiredSignoffs) {

  Page.setTitle('Scheduled Permission Changes');

  $scope.loading = true;
  $scope.failed = false;

  $scope.current_user = null;
  $scope.user_roles = [];

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

  Permissions.getScheduledChanges()
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

  $scope.signoffRequirements = [];
  PermissionsRequiredSignoffs.getRequiredSignoffs()
    .then(function(payload) {
      $scope.signoffRequirements = payload.data.required_signoffs;
    });

  $scope.$watch("ordering_str", function(value) {
    $scope.ordering = value.value.split(",");
  });

  $scope.ordering_str = {
      text: "sc_id",
      value: "sc_id"
    };

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

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };


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



   $scope.openDeleteModal = function(sc) {

    var modalInstance = $modal.open({
      templateUrl: "permission_scheduled_change_delete_modal.html",
      controller: "DeletePermissionRuleScheduledChangeCtrl",
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

  $scope.openNewScheduledPermissionChangeModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'new_user_scheduled_change_modal.html',
      controller: 'NewPermissionScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return $scope.scheduled_changes;
        },
        sc: function() {
          // blank new default release
          return {
            name: '',
            product: '',
            change_type: 'insert',
          };
        },
        permissionSignoffRequirements: function() {
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
          return "Permission";
        },
        service: function() {
          return Permissions;
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
          return {"permission": sc["permission"],
                  "username": sc["username"]};
        },
        // todo: add more stuff here
        data: function() {
          return {"options": sc["options"]};
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
          return "Permission";
        },
        service: function() {
          return Permissions;
        },
        current_user: function() {
          return $scope.current_user;
        },
        sc: function() {
          return sc;
        },
        pk: function() {
          return {"permission": sc["permission"],
                  "username": sc["username"]};
        },
        // todo: add more stuff here
        data: function() {
          return {"options": sc["options"]};
        },
      }
    });
  };

  $scope.openScheduledUpdateModal = function(sc) {

    var modalInstance = $modal.open({
      templateUrl: "permission_scheduled_change_update_modal.html",
      controller: "EditPermissionScheduledChangeCtrl",
      size: 'lg',
      backdrop: 'static',
      resolve: {
        sc: function() {
          return sc;
        }
      }
    });
  };


});
