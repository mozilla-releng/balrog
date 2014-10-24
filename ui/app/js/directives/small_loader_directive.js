// Used as a small loader animation
angular.module("app").directive('smallLoader', function() {
  return {
    scope: {},
    replace: true,
    template: [
      '<div id="spinningSquaresG" title="Loading">',
      '<div id="spinningSquaresG_1" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_2" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_3" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_4" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_5" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_6" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_7" class="spinningSquaresG">',
      '</div>',
      '<div id="spinningSquaresG_8" class="spinningSquaresG">',
      '</div>',
      '</div>'

    ].join('')
  };
});
