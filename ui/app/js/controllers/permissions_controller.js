angular.module("app").controller('PermissionsController',
function($scope, $routeParams, $location, $timeout, Permissions, Search, $modal, Page, Helpers) {

  Page.setTitle('Permissions');

  $scope.loading = true;
  $scope.failed = false;
  $scope.username = $routeParams.username;
  if ($scope.username) {
    // history of a specific rule
    Permissions.getUserPermissions($scope.username)
    .then(function(response) {
      $scope.permissions = response;
    });
  } else {
    Permissions.getUsers()
    .success(function(response) {
      $scope.users = _.map(response.users, function (each) {
        return {username: each};
      });
      $scope.permissions_count = $scope.users.length;
      $scope.page_size_pair = [{id: 20, name: '20'},
        {id: 50, name: '50'}, 
        {id: $scope.permissions_count, name: 'All'}];
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  $scope.ordering = ['username'];

  $scope.currentPage = 1;
  $scope.storedPageSize = JSON.parse(localStorage.getItem('permissions_page_size'));
  $scope.pageSize = $scope.storedPageSize? $scope.storedPageSize.id : 20;
  $scope.page_size = {id: $scope.pageSize, name: `${$scope.pageSize}`};

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

  // I don't know how else to expose this to the templates
  // $scope.getWordRegexes = Search.getWordRegexes;
  $scope.highlightSearch = Search.highlightSearch;
  // $scope.removeFilterSearchWord = Search.removeFilterSearchWord;

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
  /* End filtering */

  $scope.openUpdateModal = function(user) {
    $scope.is_edit = true;
    var modalInstance = $modal.open({
      templateUrl: 'permissions_modal.html',
      controller: 'UserPermissionsCtrl',
      backdrop: 'static',
      size: 'md',  // can be lg or md, sm
      resolve: {
        users: function () {
          return $scope.users;
        },
        is_edit: function () {
          return $scope.is_edit;
        },
        user: function () {
          return user;
        },
      }
    });
  };
  /* End openUpdateModal */

  $scope.openNewModal = function() {
    $scope.is_edit = false;
    var modalInstance = $modal.open({
      templateUrl: 'permissions_modal.html',
      controller: 'UserPermissionsCtrl',
      backdrop: 'static',
      size: 'md',
      resolve: {
        users: function () {
          return $scope.users;
        },
        is_edit: function () {
          return $scope.is_edit;
        },
        user: function () {
          return $scope.user;
        },
      }
    });
  };
    /* End openNewModal */



  $scope.openNewScheduledPermissionChangeModal = function(user) {

    var modalInstance = $modal.open({
      templateUrl: 'permissions_scheduled_change_modal.html',
      controller: 'NewPermissionScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          sc = angular.copy(user);
          sc["change_type"] = "insert";
          return sc;
        }
      }
    });
  };

  $scope.selectPageSize = function() {
    Helpers.selectPageSize($scope, 'permissions_page_size');
  };



});
