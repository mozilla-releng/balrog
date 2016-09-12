
angular.module("app").directive('loader', function() {
  return {
    scope: {},
    template: [
      '<div class="loader" title="Loading">',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '<div class="dot"></div>',
      '</div>',

    ].join('')
  };
});
