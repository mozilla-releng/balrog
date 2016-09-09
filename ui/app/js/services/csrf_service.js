angular.module("app").factory('CSRF', function($http, $q) {

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
        deferred.resolve(csrf_token);
      } else {
        $http.get('/api/csrf_token')
        .success(function(response, status, headers) {
          csrf_token = headers('X-CSRF-Token');
          timestamp = (new Date()).getTime();
          deferred.resolve(csrf_token);
        })
        .error(function() {
          deferred.reject('unable to get a CSRF token');
        });
      }
      return deferred.promise;
    },
  };
  return service;

});
