/*global: moment */

angular.module("app").directive('moment', function() {
  return {
    scope: {
      moment: '='
    },
    template: '<time title="{{ date.format(\'LLLL\') }}">{{ date.fromNow() }}</time>',
    controller: function($scope) {
      $scope.date = moment($scope.moment);
    }
  };
});
