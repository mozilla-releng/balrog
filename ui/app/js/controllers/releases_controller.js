angular.module("app").controller('ReleasesController',
function($scope, $routeParams, $location, $timeout, Releases, Search, $modal) {

  $scope.loading = true;
  $scope.failed = false;

  $scope.release_name = $routeParams.name;

  $scope.currentPage = 1;
  $scope.pageSize = 10;
  $scope.maxSize = 10;

  function loadPage(newPage) {
    Releases.getHistory($scope.release_name, $scope.pageSize, newPage)
    .success(function(response) {
      // it's the same release, but this works
      $scope.releases = response.revisions;
      $scope.releases_count = response.count;
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  if ($scope.release_name) {
    $scope.$watch("currentPage", function(newPage) {
      loadPage(newPage);
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
    ];
  }
  $scope.ordering_str = $scope.ordering_options[0];

  $scope.filters = {
    search: $location.hash(),
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
      resolve: {
        release: function () {
          return release;
        },
        diff: function() {
          return false;
        }
      }
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
  };
  /* End openDataModal */

  $scope.openUpdateModal = function(release) {

    var modalInstance = $modal.open({
      templateUrl: 'release_modal.html',
      controller: 'ReleaseEditCtrl',
      // size: size,  // can be lg or sm
      resolve: {
        release: function () {
          return release;
        }
      }
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
