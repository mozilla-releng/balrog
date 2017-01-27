angular.module("app").controller("PermissionScheduledChangesController",
function($scope, $routeParams, $location, $timeout, Permissions, Rules, Search, $modal, $route, Releases) {

  $scope.loading = true;
  $scope.failed = false;



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
      text: "username",
      value: "username"
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

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };

  $scope.$watchCollection('filters.search', function(value) {
    $location.hash(value);
    Search.noticeSearchChange(
      value,
      ['username']
    );
  });

  $scope.filterBySearch = function(item) {
    // basically, look for a reason to NOT include this
    if (Search.word_regexes.length) {
      // every word in the word_regexes array needs to have some match
      var matches = 0;
      _.each(Search.word_regexes, function(each) {
        var regex = each[0];
        var on = each[1];
        // console.log(regex, on);
        if ((on === '*' || on === 'username') && item.username && item.username.match(regex)) {
          matches++;
          return;
        }
      });
      return matches === Search.word_regexes.length;
    }

    return true;  // include it
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

  $scope.formatMoment = function(when) {
    date = moment(when);
    // This is copied from app/js/directives/moment_directive.js
    // We can't use that for this page, because it doesn't re-render when
    // values change.
    return '<time title="' + date.format('dddd, MMMM D, YYYY HH:mm:ss ') + 'GMT' + date.format('ZZ') + '">' + date.fromNow() + '</time>';
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
        }
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
          sc.when = new Date(sc.when) + 100;
          return sc;
        }
      }
    });
  };


});
