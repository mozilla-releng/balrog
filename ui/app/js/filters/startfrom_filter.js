
angular.module("app").filter('startFrom', function() {
    return function(input, start) {
        if (angular.isUndefined(input)) {
          return input;
        }
        start = +start; //parse to int
        return input.slice(start);
    };
});
