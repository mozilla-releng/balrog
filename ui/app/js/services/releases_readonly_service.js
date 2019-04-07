angular.module('app').factory('ReleasesReadonly', function($http, ScheduledChanges) {
    var services = {
        getReleasesReadonly: function() {

        },

        makeReadonly: function(releaseReadonly, csrf_token) {

        },

        makeReadWrite: function(releaseReadonly, csrf_token) {

        },

        signoff: function(sc_id, csrf_token) {

        },

        revokeSignoff: function(sc_id, csrf_token) {

        }
    };

    return services;
});