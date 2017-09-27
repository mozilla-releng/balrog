angular.module("app").directive('showSignoffRequirements', function() {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      requirements: '=',
    },
    template: '<div ng-show="requirements.length" class="has-error">' +
      '<p class="help-block">' +
      'This change requires signoffs: ' +
      "<span ng-repeat=\"(key, value) in requirements.roles\">{{ value }} from {{ key }}{{$last ? '.' : ', '}}</span>" +
      '</p>' +
      '</div>',
  };
});
