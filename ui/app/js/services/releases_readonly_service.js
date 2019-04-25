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
            when = new Date();
            when.setSeconds(when.getSeconds() + 10);

            data = angular.copy(release_readonly);
            data.change_type = 'delete';
            data.csrf_token = csrf_token;
            data.when = when.getTime();

            return $http.post('/api/scheduled_changes/releases_readonly', data);
        },

        scheduledChanges: function() {
            return $http.get('/api/scheduled_changes/releases_readonly');
        },

        signoff: function(sc_id, csrf_token) {

        },

        revokeSignoff: function(sc_id, csrf_token) {

        }
    };

    return services;
});