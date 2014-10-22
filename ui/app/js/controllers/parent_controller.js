/*global: sweetAlert */

/* a middleware the sniffs on AJAX errors */
angular.module("app").factory('errorSniffer', ['$q', function($q) {
  return {
    responseError: function(rejection) {
      if (rejection.status === 401) {
        // Unauthorized
        sweetAlert("Unauthorized", rejection.data, "error");
      } else if (rejection.status === 500) {
        sweetAlert(
          "Internal Server Error",
          "An unexpected server error happened. See the console log for more details.",
          "error"
        );
        console.warn(rejection.status, rejection.data);
      // } else {
      //   console.warn(rejection.status);
      }
      return $q.reject(rejection);
    }
  };
}]);

angular.module("app").config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('errorSniffer');
}]);


/* Put things in here that the sub-controllers can use */
angular.module("app").controller('ParentController',
function($scope) {

  // function escapeRegExp(string){
  //   return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  // }

});
