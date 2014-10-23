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
    getReleases: function() {
      return $http.get('/api/releases');
    },
    getHistory: function(name) {
      return $http.get('/api/releases/' + name + '/revisions');
    },
    getRelease: function(name) {
      return $http.get('/api/releases/' + name);
    },
    updateRelease: function(name, data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.put('/api/releases/' + name, data);
    },
    deleteRelease: function(name, data, csrf_token) {
      var url = '/api/releases/' + name;
      url += '?data_version=' + data.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    addRelease: function(data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.post('/api/releases', data);
    },
    revertRelease: function(name, change_id, csrf_token) {
      var data = {change_id: change_id};
      data.csrf_token = csrf_token;
      return $http.post('/api/releases/' + name + '/revisions', data);
    }
  };
  return service;

});
