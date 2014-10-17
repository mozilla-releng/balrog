angular.module("app").factory('ReleasesService', function($http, $q) {
  var service = {
    getNames: function() {
      var deferred = $q.defer();
      $http.get('/api/releases?names_only=1')
      .success(function(response) {
        deferred.resolve(response.names);
      }).error(function(){
        console.error(arguments);
        deferred.reject(arguments);
      });
      return deferred.promise;
    },
  };
  return service;

});
