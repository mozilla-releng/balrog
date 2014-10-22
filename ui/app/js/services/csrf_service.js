angular.module("app").factory('CSRFService', function($http, $q) {
  // these routes map to stubbed API endpoints in config/server.js
  var csrf_token = null;
  var timestamp = null;

  function notTooOld(seconds) {
    var diff = (new Date()).getTime() - timestamp;
    return (diff / 1000) < seconds;
  }

  var service = {
    getToken: function() {
      var deferred = $q.defer();
      if (csrf_token !== null && notTooOld(60 * 60)) {
        // console.log('Reusing csrf_token', csrf_token);
        deferred.resolve(csrf_token);
      } else {
        // console.log('Fetching new csrf_token');
        $http.get('/api/csrf_token')
        .success(function(response, status, headers) {
          csrf_token = headers('X-CSRF-Token');
          // console.log('Fetched csrf_token', csrf_token);
          timestamp = (new Date()).getTime();
          deferred.resolve(csrf_token);
        }).error(function() {
          deferred.reject('unable to get a CSRF token');
        });
      }
      return deferred.promise;
    },
  };
  return service;

});
