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
    getScheduledChanges: function() {
      return $http.get("/api/scheduled_changes/permissions?all=1");
    },
    addScheduledChange: function(data, csrf_token) {
      data = jQuery.extend({}, data);
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/permissions", data);
    },

    getUserRoles: function(username) {
      // What comes back from the server is a dict like this:
      //  {'roles': ['role1', 'role2'...]} if the user has roles
      // otherwise the value of the dict will be an empty array:
      //  {'roles': []}
      // when the user has no roles
      var url = '/api/users/' + encodeURIComponent(username) + '/roles';
      return $http.get(url);
    },
    getAllRoles: function() {
      return $http.get('/api/users/roles');
    },
    grantRole: function(username, role, data_version, csrf_token) {
      var url = '/api/users/' + encodeURIComponent(username) + '/roles/';
      url += encodeURIComponent(role);
      return $http.put(url);
    },
    revokeRole: function(username, role, csrf_token) {
      var url = '/api/users/' + encodeURIComponent(username) + '/roles/';
      url += encodeURIComponent(role.role);
      url += '?data_version=' + role.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
     deleteScheduledChange: function(sc_id, data, csrf_token) {
      var url = "/api/scheduled_changes/permissions/" + sc_id;
      url += '?data_version=' + data.sc_data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
     },
     updateScheduledChange: function(sc_id, data, csrf_token) {
      data = jQuery.extend({}, data);
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/permissions/" + sc_id, data);
    },

  };
  return service;

});
