angular.module("app").controller('PermissionsController',
function($scope, $routeParams, $location, $timeout, Permissions, Search, $modal) {

  $scope.loading = true;
  $scope.failed = false;

  $scope.username = $routeParams.username;
  if ($scope.username) {
    // history of a specific rule
    Permissions.getUserPermissions($scope.username)
    .success(function(response) {
      $scope.permissions = response.permissions; //????
    })
    .error(function() {
      console.error(arguments);
    });
  } else {
    Permissions.getUsers()
    .success(function(response) {
      $scope.users = _.map(response.users, function (each) {
        return {username: each};
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

  $scope.ordering = ['username'];

  $scope.currentPage = 1;
  $scope.pageSize = 10;  // default

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return false || $scope.filters.search.length;
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

    var modalInstance = $modal.open({
      templateUrl: 'permissions_modal.html',
      controller: 'UserPermissionsCtrl',
      // size: size,  // can be lg or sm
      resolve: {
        user: function () {
          return user;
        }
      }
    });


  };
  /* End openUpdateModal */

  $scope.openNewModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'user_modal.html',
      controller: 'NewUserCtrl',
      // size: 'sm',
      resolve: {
        users: function () {
          return $scope.users;
        }
      }
    });

    modalInstance.result.then(function (user) {
      $scope.users.push(user);
      $scope.openUpdateModal(user);
    }, function () {
      // modal closed
    });

  };
  /* End openNewModal */



});
