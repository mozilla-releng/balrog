angular.module("app").directive('showSignoffRequirements', function() {
  return {
    restrict: 'E',
    replace: true,
    scope: {
      requirements: '=',
    },
    template: '<div ng-show="requirements.length" class="has-error">' +
      '<p class="help-block">' +
      'Making this change requires signoffs and therefore must be a scheduled change.' +
      '</p>' +
      '</div>',
  };
});
