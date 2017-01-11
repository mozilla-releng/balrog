angular.module("app").controller("ReleaseScheduledChangesController",
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route, Releases) {

  $scope.loading = true;
  $scope.failed = false;

  $scope.sc_id = $routeParams.sc_id;

  function loadPage(newPage) {
    Releases.getScheduledChangeHistory($scope.sc_id, $scope.pageSize, newPage)
    .success(function(response) {
      // it's the same release, but this works
      $scope.scheduled_changes = response.revisions;
      $scope.scheduled_changes_count = response.count;
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
    $scope.$watch("currentPage", function(newPage) {
      loadPage(newPage);
    });
  } else {

  Releases.getScheduledChanges()
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
      text: "Product, Name",
      value: "product, Name"
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

  $scope.formatMoment = function(when) {
    date = moment(when);
    // This is copied from app/js/directives/moment_directive.js
    // We can't use that for this page, because it doesn't re-render when
    // values change.
    return '<time title="' + date.format('dddd, MMMM D, YYYY HH:mm:ss ') + 'GMT' + date.format('ZZ') + '">' + date.fromNow() + '</time>';
  };

  $scope.openNewScheduledReleaseChangeModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'release_scheduled_change_modal.html',
      controller: 'NewReleaseScheduledChangeCtrl',
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

  $scope.openUpdateModal = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "release_scheduled_change_modal.html",
      controller: "EditReleaseScheduledChangeCtrl",
      size: 'lg',
      backdrop: 'static',
      resolve: {
        sc: function() {
          sc.when = new Date(sc.when);
          return sc;
        }
      }
    });
  };

  $scope.openDeleteModal = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "release_scheduled_change_delete_modal.html",
      controller: "DeleteReleaseScheduledChangeCtrl",
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
});
