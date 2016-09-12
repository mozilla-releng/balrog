angular.module("app").directive('saveSearch', function($location, $localForage) {
  return {
    restrict: 'AE',
    replace: true,
    scope: {
      input: '=',
      results: '='
    },
    template: '<a href="#" class="btn btn-default btn-xs save-search" ' +
              'ng-click="save()" ' +
              'ng-show="input.length">' +
              '<span ng-bind="saved ? \'Search saved\' : \'Save this search\'">' +
              '</span> ' +
              '<i class="glyphicon glyphicon-floppy-disk" ' +
              'ng-class="{\'glyphicon-floppy-disk\': !saved, ' +
              '\'glyphicon-floppy-saved\': saved}"></i>' +
              '</a>' ,
    controller: function($scope) {
      $scope.$watch('input', function(value) {
        $scope.saved = !!_.find($scope.savedSearches, {
          input: value,
          path: $location.path()
        });
      });
      $scope.saved = false;
      $scope.savedSearches = [];
      $localForage.getItem('savedSearches').then(function(data) {
        if (data) {
          $scope.savedSearches = data;
          $scope.saved = !!_.find($scope.savedSearches, {
            input: $scope.input,
            path: $location.path()
          });
        }
      });
      $scope.save = function() {
        var found = !!_.find($scope.savedSearches, {
          input: $scope.input,
          path: $location.path()
        });
        if (found) {
          // already saved it, remove it then
          $scope.savedSearches = _.filter($scope.savedSearches, function(search) {
            return !(search.input === $scope.input && search.path === $location.path());
          });
          $scope.saved = false;
        } else {
          $scope.savedSearches.unshift({
            input: $scope.input,
            results: $scope.results,
            path: $location.path(),
            hash: $location.hash()
          });
          $scope.saved = true;
        }
        // save a max of 10 elements
        $localForage.setItem('savedSearches', $scope.savedSearches.slice(0, 10));
      };
    }
  };
});
