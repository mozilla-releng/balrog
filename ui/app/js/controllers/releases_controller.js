angular.module("app").controller('ReleasesController',
function($scope, $routeParams, $location, $timeout, Releases, Search, $modal) {

  $scope.loading = true;
  $scope.failed = false;

  $scope.release_name = $routeParams.name;
  if ($scope.release_name) {

    Releases.getHistory($scope.release_name)
    .success(function(response) {
      console.log(response);
      // it's the same release, but this works
      $scope.releases = response.revisions;
      $scope.count = response.count;
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  } else {
    Releases.getReleases()
    .success(function(response) {
      $scope.releases = response.releases;
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
        text: "Data Version",
        value: "-data_version"
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
      {
        text: "Version",
        value: "version"
      },
      {
        text: "Version (reverse)",
        value: "-version"
      },
    ];
  }
  $scope.ordering_str = $scope.ordering_options[0];

  $scope.currentPage = 1;
  $scope.pageSize = 10;  // default

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return false || $scope.filters.search.length;
  };

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  // We don't want to immediately start searching on every typed
  // little character. Instead, bunch them up and search after a
  // little 200ms pause.
  var filters_search_timeout = null;
  var filters_search_temp = '';
  $scope.$watchCollection('filters.search', function(value) {
    // break up every entered word into a word delimited regex
    if (filters_search_timeout) {
      $timeout.cancel(filters_search_timeout);
    }
    filters_search_temp = value;
    filters_search_timeout = $timeout(function() {
      $scope.filters.search_actual = filters_search_temp;
    }, 300);
  });

  $scope.$watchCollection('filters.search_actual', function(value) {
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
        if ((on === '*' || on === 'version') && release.version && release.version.match(regex)) {
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
      resolve: {
        release: function () {
          return release;
        },
        diff: function() {
          return false;
        }
      }
    });
    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openDataModal */

  $scope.openDiffModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_data_modal.html',
      controller: 'ReleaseDataCtrl',
      size: 'lg',
      resolve: {
        release: function () {
          return release;
        },
        diff: function() {
          return true;
        }
      }
    });
    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openDataModal */

  $scope.openUpdateModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_modal.html',
      controller: 'ReleaseEditCtrl',
      // size: size,  // can be lg or sm
      resolve: {
        // items: function () {
        //   return $scope.items;
        // },
        release: function () {
          return release;
        }
      }
    });
    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openUpdateModal */

  $scope.openDeleteModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_delete_modal.html',
      controller: 'ReleaseDeleteCtrl',
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

    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openDeleteModal */

  $scope.openNewReleaseModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'release_modal.html',
      controller: 'NewReleaseCtrl',
      // size: 'sm',
      resolve: {
        releases: function() {
          return $scope.releases;
        },
      }
    });

    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openNewReleaseModal */

  $scope.openRevertModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_revert_modal.html',
      controller: 'ReleaseRevertCtrl',
      // size: 'sm',
      resolve: {
        release: function () {
          return release;
        }
      }
    });

    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
      $location.path('/releases');
    }, function () {
      // console.log('modal closed');
    });
  };
  /* End openDeleteModal */

});
