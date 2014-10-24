angular.module("app").factory('Permissions', function($http, $q) {
  var service = {
    getUsers: function() {
      return $http.get('/api/users');
    },
    getUserPermissions: function(username) {
      var deferred = $q.defer();
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      $http.get(url)
      .success(function(response) {
        // What comes back from the server is a dict like this:
        //  {permission1: {options: ...}, otherPermission: {options: ...}, ...}
        // so turn it into a list with the key being called "permission"
        var permissions = _.map(response, function(value, key) {
          value.permission = key;
          return value;
        });
        deferred.resolve(permissions);
      })
      .error(function() {
        console.error(arguments);
        deferred.reject(arguments);
      });
      return deferred.promise;
    },
    addPermission: function(username, data, csrf_token) {
      data.csrf_token = csrf_token;
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      url += '/' + encodeURIComponent(data.permission);
      return $http.put(url, data);
    },
    updatePermission: function(username, data, csrf_token) {
      data.csrf_token = csrf_token;
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      url += '/' + encodeURIComponent(data.permission);
      return $http.post(url, data);
    },
    deletePermission: function(username, data, csrf_token) {
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      url += '/' + encodeURIComponent(data.permission);
      url += '?data_version=' + data.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
  };
  return service;

});
