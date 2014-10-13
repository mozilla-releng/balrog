angular.module("app").controller('RulesController',
function($scope, $location, RulesService) {

  $scope.filters = {};

  RulesService.getRules()
  .success(function(data) {
    $scope.rules = data.rules;
    $scope.total_count = data.count;
  }).error(function() {
    console.error(arguments);
  });

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  var word_regexes = [];
  $scope.$watch('filter.search', function(value) {
    // break up every entered word into a word delimited regex
    word_regexes = [];
    if (value) {
      _.each(value.split(' '), function(term) {
        word_regexes.push(
          new RegExp('\\b' + escapeRegExp(term), 'i')
        );
      });
    }
  });

  $scope.filterBySearch = function(rule) {
    // basically, look for a reason to NOT include this
    if (word_regexes.length) {
      // if there's no match on either of them, return false
      console.log('regexes', word_regexes);

      var matched = false;
      _.each(word_regexes, function(regex) {
        if (rule.product.match(regex)) {
          matched = true;
        } else {
          matched = false;
        }
        if (rule.channel.match(regex)) {
          matched = true;
        } else {
          matched = false;
        }
      });
      // no match or early escape
      return matched;
    }
    return true;  // include it
  };
  // $scope.credentials = { username: "", password: "" };
  //
  // var onLoginSuccess = function() {
  //   $location.path('/home');
  // };
  //
  // $scope.login = function() {
  //   AuthenticationService.login($scope.credentials).success(onLoginSuccess);
  // };
});
