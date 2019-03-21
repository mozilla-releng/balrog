angular.module("app").factory('Permissions', function($http, $q, ScheduledChanges, Helpers, PermissionsRequiredSignoffs) {
  var service = {
    getUsers: function() {
      return $http.get('/api/users');
    },
    getUserInfo: function(username) {
      var deferred = $q.defer();
      var url = '/api/users/' + encodeURIComponent(username);
      // TODO: can probably remove this header setting because we use headers.common.blah now
      $http.get(url, config={"headers": {"X-Authorization": "Bearer " + localStorage.getItem("accessToken")}})
      .success(function(response) {
        // What comes back from the server is a dict like this:
        //  {permission1: {options: ...}, otherPermission: {options: ...}, ...}
        // so turn it into a list with the key being called "permission"
        var permissions = _.map(response.permissions, function(value, key) {
          value.permission = key;
          return value;
        });
        deferred.resolve({"permissions": permissions, "roles": response.roles});
      })
      .error(function(response) {
        deferred.reject(response.detail);
      });
      return deferred.promise;
    },
    addPermission: function(username, data, csrf_token) {
      data.csrf_token = csrf_token;
      data = Helpers.replaceEmptyStrings(data);
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      url += '/' + encodeURIComponent(data.permission);
      return $http.put(url, data);
    },
    updatePermission: function(username, data, csrf_token) {
      data.csrf_token = csrf_token;
      data = Helpers.replaceEmptyStrings(data);
      var url = '/api/users/' + encodeURIComponent(username) + '/permissions';
      url += '/' + encodeURIComponent(data.permission);
      return $http.put(url, data);
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
      data = Helpers.replaceEmptyStrings(data);
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/permissions", data);
    },

    grantRole: function(username, role, data_version, csrf_token) {
      var url = '/api/users/' + encodeURIComponent(username) + '/roles/';
      url += encodeURIComponent(role);
      return $http.put(url, {'csrf_token': csrf_token});
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
      data = Helpers.replaceEmptyStrings(data);
      return $http.post("/api/scheduled_changes/permissions/" + sc_id, data);
    },
    signoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("permissions", sc_id);
      return $http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("permissions", sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return $http.delete(url, data);
    },
    permissionSignoffsRequired: function(oldPermission, newPermission, permissionSignoffRequirements) {
      function matchesPermission(permission, permissionSignoffRequirement) {
        var options = permission.options;
        var hasProducts = options && options.products && options.products.length > 0;
        var matchesProduct = options && options.products && options.products.indexOf(permissionSignoffRequirement.product) !== -1;
        return !hasProducts || matchesProduct;
      }

      function matchesPermissions(permissionSignoffRequirement) {
        // oldPermission is undefined during create. newPermission is
        // undefined during delete.
        var permissions = [oldPermission, newPermission].filter(function(permission) { return permission; });
        return permissions.some(function(permission) { return matchesPermission(permission, permissionSignoffRequirement); });
      }

      var relevantRequirements = permissionSignoffRequirements.filter(matchesPermissions);
      return PermissionsRequiredSignoffs.convertToMap(relevantRequirements);
    },
  };
  return service;

});
