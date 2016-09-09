/*global: moment */

angular.module("app").directive('moment', function() {
  return {
    scope: {
      moment: '='
    },
    template: '<time title="{{ date.format(\'dddd, MMMM D, YYYY HH:mm:ss \') + \'GMT\' + date.format(\'ZZ\') }}">{{ date.fromNow() }}</time>',
    controller: function($scope) {
      $scope.date = moment($scope.moment);
    }
  };
});
