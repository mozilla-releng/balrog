angular.module("app").factory('Releases', function($http, $q, ScheduledChanges, Helpers, GCSConfig) {
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
    getHistory: function(name, product) {
      var deferred = $q.defer();
      var releases = [];
      var bucket = null;
      if (name.includes('nightly')) {
        bucket = GCSConfig['nightly_history_bucket'];
      }
      else {
        bucket = GCSConfig['releases_history_bucket'];
      }

      var baseUrl = bucket + '?prefix=' + name + '/' + '&delimeter=/';

      function parseReleases(raw_releases) {
        if (raw_releases) {
          raw_releases.forEach(function(r) {
            var parts = r.name.replace(name + "/", "").replace(".json", "").split("-");
            var release = {
              "name": name,
              "product": product,
              // Sometimes data version in None, which will show up as NaN. Meh?
              "data_version": parseInt(parts[0]),
              "timestamp": parseInt(parts[1]),
              "changed_by": parts[2],
              "data_url": r.mediaLink,
            };
            releases.push(release);
          });
        }
      }

      function getReleases(url, pageToken) {
        var fullUrl = url;
        if (pageToken) {
          fullUrl += "&pageToken=" + pageToken;
        }
        $http.get(fullUrl)
        .success(function(response) {
          parseReleases(response.items);
          if (response.nextPageToken) {
            getReleases(url, response.nextPageToken);
          }
          else {
            // descending sort, so newer versions appear first
            releases.sort(function(a, b) {
              return a.data_version < b.data_version;
            });
            deferred.resolve(releases);
          }
        })
        .error(function() {
          console.error(arguments);
          deferred.reject(arguments);
        });
      }

      getReleases(baseUrl);
      return deferred.promise;
    },
    getRelease: function(name) {
      return $http.get('/api/releases/' + encodeURIComponent(name));
    },
    getReadOnly: function(name) {
      return $http.get('/api/releases/' + encodeURIComponent(name) + '/read_only');
    },
    getData: function(link) {
      var deferred = $q.defer();
      $http.get(link)
      .success(function(response) {
        deferred.resolve(stringify(response, { cmp: function(a, b) { return a.key < b.key ? -1 : 1; }, space: 2 }));
      })
      .error(function() {
        deferred.reject(arguments);
      });
      return deferred.promise;
    },
    getUpDiff: function(sc_id) {
      var url = '/api/scheduled_change/diff/release/' + sc_id;
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
