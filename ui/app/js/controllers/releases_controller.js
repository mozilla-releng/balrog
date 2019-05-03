angular.module("app").controller('ReleasesController',
function($scope, $routeParams, $location, $timeout, Releases, Search, $modal, Page, Helpers, Auth0) {

  Page.setTitle('Releases');

  $scope.loading = true;
  $scope.failed = false;
  $scope.release_name = $routeParams.name;
  $scope.storedPageSize = JSON.parse(localStorage.getItem('releases_page_size'));
  $scope.pageSize = $scope.storedPageSize? $scope.storedPageSize.id : 20;
  $scope.page_size = {id: $scope.pageSize, name: $scope.storedPageSize? $scope.storedPageSize.name : $scope.pageSize};
  $scope.currentPage = 1;
  $scope.maxSize = 10;
  $scope.auth0 = Auth0;

  if ($scope.release_name) {
    Releases.getHistory($scope.release_name)
    .then(function(response, err) {
      if (err) {
        sweetAlert("Failed to load release revisions:", err);
      }
      else {
        $scope.releases = response;
        $scope.releases_count = response.length;
        $scope.loading = false;
      }
    });
  } else {
    Releases.getReleases()
    .success(function(response) {
      $scope.releases = response.releases;
      $scope.releases.forEach(function(release) {
        // Ideally we'd convert this field to a Map, but we can't use
        // Maps, so let's match the structure returned by
        // RulesService#ruleSignoffsRequired.
        var oldSignoffs = release.required_signoffs;
        release.required_signoffs = {length: Object.keys(oldSignoffs).length, roles: oldSignoffs};
      });
      $scope.releases_count = response.releases.length;
      $scope.page_size_pair = [{id: 20, name: '20'},
        {id: 50, name: '50'}, 
        {id: $scope.releases_count, name: 'All'}];
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  $scope.$watch('ordering_str', function(value) {
    $scope.ordering = value.value.split(',');
  });
  if ($scope.release_name) {
    $scope.ordering_options = [
      {
        text: "Timestamp",
        value: "-timestamp"
      },
    ];
  } else {
    $scope.ordering_options = [
      {
        text: "Name",
        value: "name"
      },
      {
        text: "Product",
        value: "product"
      },
      {
        text: "Product (reverse)",
        value: "-product"
      },
    ];
  }
  $scope.ordering_str = $scope.ordering_options[0];

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.selectPageSize = function() {
    Helpers.selectPageSize($scope, 'releases_page_size');
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  $scope.$watchCollection('filters.search', function(value) {
    $location.hash(value);
    Search.noticeSearchChange(
      value,
      ['product', 'channel', 'mapping']
    );
  });

  // I don't know how else to expose this to the templates
  $scope.getWordRegexes = Search.getWordRegexes;
  $scope.highlightSearch = Search.highlightSearch;
  $scope.removeFilterSearchWord = Search.removeFilterSearchWord;

  $scope.filterBySearch = function(release) {
    // basically, look for a reason to NOT include this
    if (Search.word_regexes.length) {
      // every word in the word_regexes array needs to have some match
      var matches = 0;
      _.each(Search.word_regexes, function(each) {
        var regex = each[0];
        var on = each[1];
        // console.log(regex, on);
        if ((on === '*' || on === 'product') && release.product && release.product.match(regex)) {
          matches++;
          return;
        }
        if ((on === '*' || on === 'mapping') && release.name && release.name.match(regex)) {
          matches++;
          return;
        }
      });
      return matches === Search.word_regexes.length;
    }

    return true;  // include it
  };
  /* End filtering */

  $scope.openDataModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_data_modal.html',
      controller: 'ReleaseDataCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        release: function () {
          return release;
        },
        previous_version: function() {
          return null;
        },
        diff: function() {
          return false;
        },
      }
    });
  };
  /* End openDataModal */

  $scope.openDiffModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_data_modal.html',
      controller: 'ReleaseDataCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        release: function () {
          return release;
        },
        previous_version: function() {
          var i = $scope.releases.indexOf(release);
          if (i === $scope.releases.length-1) {
            return null;
          }
          else {
            return $scope.releases[i+1];
          }
        },
        diff: function() {
          return true;
        },
      }
    });
  };
  /* End openDataModal */

  $scope.openUpdateModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_modal.html',
      controller: 'ReleaseEditCtrl',
      backdrop: 'static',
      // size: size,  // can be lg or sm
      resolve: {
        release: function () {
          return release;
        }
      }
    });
  };
  /* End openUpdateModal */

  $scope.openNewScheduledDeleteModal = function(release) {
    var modalInstance = $modal.open({
      templateUrl: 'release_scheduled_delete_modal.html',
      controller: 'NewReleaseScheduledDeleteCtrl',
      size: 'lg',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          sc = angular.copy(release);
          sc["change_type"] = "delete";
          return sc;
        }
      }
    });
  };

  $scope.openNewScheduledReleaseChangeModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_scheduled_change_modal.html',
      controller: 'NewReleaseScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          sc = angular.copy(release);
          sc["change_type"] = "update";
          return sc;
        }
      }
    });
  };

  $scope.openDeleteModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_delete_modal.html',
      controller: 'ReleaseDeleteCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        release: function () {
          return release;
        },
        releases: function() {
          return $scope.releases;
        },
      }
    });
  };
  /* End openDeleteModal */

  $scope.openNewReleaseModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'release_modal.html',
      controller: 'NewReleaseCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        releases: function() {
          return $scope.releases;
        },
      }
    });
  };
  /* End openNewReleaseModal */

  $scope.openRevertModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_revert_modal.html',
      controller: 'ReleaseRevertCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        release: function () {
          return release;
        }
      }
    });

    modalInstance.result.then(function () {
      $location.path('/releases');
    }, function () {
      // modal closed
    });
  };
  /* End openDeleteModal */

  $scope.openReadOnlyModal = function (release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_read_only_modal.html',
      controller: 'ReleaseReadOnlyCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        release: function() {
          return release;
        }
      }
    });

    modalInstance.result.then(function () {
      $location.path('/releases');
    }, function () {
      // modal closed
    });
  };
  /* End openReadOnlyModal */
});
