angular.module('app').factory('ReleasesReadonly', function($http, ScheduledChanges) {
    var services = {
        getReleaseReadonly: function(release_name) {
            return $http.get('/api/releases_readonly/' + encodeURIComponent(release_name));
        },

        makeReadonly: function(release_name, csrf_token) {
            data = {
                csrf_token: csrf_token
            };
            return $http.post('/api/releases_readonly/' + encodeURIComponent(release_name), data);
        },

        makeReadWrite: function(release_name, data_version, csrf_token) {
            config = {
                params: {
                    data_version: data_version,
                    csrf_token: csrf_token
                }
            };
            return $http.delete('/api/releases_readonly/' + encodeURIComponent(release_name), config);
        },
        
        scheduleReadWriteReleaseChange: function(release_readonly, csrf_token) {
            data = angular.copy(release_readonly);
            data.change_type = 'delete';
            data.csrf_token = csrf_token;

            return $http.post('/api/scheduled_changes/releases_readonly', data);
        },

        scheduledChanges: function() {
            return $http.get('/api/scheduled_changes/releases_readonly');
        },

        deleteScheduledChange: function(sc_id, data, csrf_token) {
            var url = "/api/scheduled_changes/releases_readonly/" + sc_id;
            url += '?data_version=' + data.sc_data_version;
            url += '&csrf_token=' + encodeURIComponent(csrf_token);
            return $http.delete(url);
        },

        signoffOnScheduledChange: function(sc_id, data) {
            var url = ScheduledChanges.signoffsUrl("releases_readonly", sc_id);
            return $http.post(url, data);
        },

        revokeSignoffOnScheduledChange: function(sc_id, data) {
            var url = ScheduledChanges.signoffsUrl("releases_readonly", sc_id);
            url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
            return $http.delete(url, data);
        }
    };

    return services;
});