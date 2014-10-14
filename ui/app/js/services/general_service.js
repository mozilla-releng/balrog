// angular.module("app").config(function($httpProvider){
//   $httpProvider.defaults.headers.put['Content-Type'] = 'multipart/form-data';
// });

angular.module("app").factory('GeneralService', function($http) {
  // these routes map to stubbed API endpoints in config/server.js
  // var csrf_token = null;
  var service = {
    getCSRFToken: function() {
      return $http.get('/api/csrf_token');
    },
  };
  return service;

});
