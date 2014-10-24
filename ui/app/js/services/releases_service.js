angular.module("app").factory('Releases', function($http, $q) {
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
      url = '/api/releases/' + name + '/revisions';
      url += '?limit=100';
      return $http.get(url);
    },
    getRelease: function(name) {
      return $http.get('/api/releases/' + name);
    },
    getData: function(change_id) {
      var url = '/api/history/view/release/' + change_id + '/data';
      return $http.get(url);
    },
    getDiff: function(change_id) {
      var url = '/api/history/diff/release/' + change_id + '/data';
      return $http({
        url: url,
        method: 'GET',
        transformResponse: function(value) {
          // If we don't do this, angular is going to try
          // to parse the data as JSON just because it's
          // a string.
          return value;
        }
      });
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
