angular.module("app").factory('Releases', function($http, $q, ScheduledChanges, Helpers) {
  var service = {
    getNames: function() {
      var deferred = $q.defer();
      $http.get('/api/releases?names_only=1')
      .success(function(response) {
        deferred.resolve(response.names);
      })
      .error(function(){
        console.error(arguments);
        deferred.reject(arguments);
      });
      return deferred.promise;
    },
    getReleases: function() {
      return $http.get('/api/releases');
    },
    getProducts: function(){
      return $http.get('/api/releases/columns/product');
    },
    getHistory: function(name, limit, page) {
      url = '/api/releases/' + encodeURIComponent(name) + '/revisions';
      url += '?limit=' + limit + '&page=' + page;
      return $http.get(url);
    },
    getRelease: function(name) {
      return $http.get('/api/releases/' + encodeURIComponent(name));
    },
    getReadOnly: function(name) {
      return $http.get('/api/releases/' + encodeURIComponent(name) + '/read_only');
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
      data = Helpers.replaceEmptyStrings(data);
      return $http.put('/api/releases/' + encodeURIComponent(name), data);
    },
    changeReadOnly: function(name, data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.put('/api/releases/' + encodeURIComponent(name) + '/read_only', data);
    },
    deleteRelease: function(name, data, csrf_token) {
      var url = '/api/releases/' + encodeURIComponent(name);
      url += '?data_version=' + data.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    addRelease: function(data, csrf_token) {
      data.csrf_token = csrf_token;
      data = Helpers.replaceEmptyStrings(data);
      return $http.post('/api/releases', data);
    },
    revertRelease: function(name, change_id, csrf_token) {
      var data = {change_id: change_id};
      data.csrf_token = csrf_token;
      var url = '/api/releases/' + encodeURIComponent(name) + '/revisions';
      return $http.post(url, data);
    },

    getScheduledChanges: function() {
      return $http.get("/api/scheduled_changes/releases?all=1");
    },

    getScheduledChange: function(sc_id) {
      return $http.get("/api/scheduled_changes/releases/" + sc_id);
    },
    getScheduledChangeHistory: function(sc_id, limit, page) {
      url = '/api/scheduled_changes/releases/' + encodeURIComponent(sc_id) + '/revisions';
      url += '?limit=' + limit + '&page=' + page;
      return $http.get(url);
    },

    addScheduledChange: function(data, csrf_token) {
      data = jQuery.extend({}, data);
      data = Helpers.replaceEmptyStrings(data);
      if (!!data.when) {
        data.when = data.when.getTime();
      }
      else {
        data.when = null;
      }
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/releases", data);
    },

    updateScheduledChange: function(sc_id, data, csrf_token) {
      data = jQuery.extend({}, data);
      data = Helpers.replaceEmptyStrings(data);
      if (!!data.when) {
        data.when = data.when.getTime();
      }else{
        data.when = null;
      }
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/releases/" + sc_id, data);
    },

    deleteScheduledChange: function(sc_id, data, csrf_token) {
      var url = "/api/scheduled_changes/releases/" + sc_id;
      url += '?data_version=' + data.sc_data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
     },

    signoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("releases", sc_id);
      return $http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("releases", sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return $http.delete(url, data);
    },
  };

  return service;

});
