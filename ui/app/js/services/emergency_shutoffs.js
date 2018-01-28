angular.module('app').factory('EmergencyShutoffs', function($http) {
    var service = {
        getEmergencyShutoffs: function() {
            return $http.get('/api/emergency_shutoff')
        },
        createEmergencyShutoff: function(product, channel) {
            data = {product, channel};
            return $http.post('/api/emergency_shutoff', data);
        },
        scheduleEnableUpdates: function(sc, csrf_token) {
            data = jQuery.extend({}, sc);
            data.when = data.when.getTime();
            data.csrf_token = csrf_token;
            return $http.post("/api/scheduled_changes/emergency_shutoff", data);
        }
    };

    return service;
});