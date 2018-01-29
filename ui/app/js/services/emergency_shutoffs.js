angular.module('app').factory('EmergencyShutoffs', function($http, ScheduledChanges) {
  var service = {
    get: function() {
      return $http.get('/api/emergency_shutoff')
    },
    create: function(product, channel) {
      data = {product, channel};
      return $http.post('/api/emergency_shutoff', data);
    },
    delete: function(product, channel, data_version, csrf_token) {
      return $http.delete(
          `/api/emergency_shutoff/${product}/${channel}?data_version=${data_version}&csrf_token=${encodeURIComponent(csrf_token)}`);
    },
    scheduledChanges: function() {
      return $http.get('/api/scheduled_changes/emergency_shutoff');
    },
    scheduleEnableUpdates: function(sc, csrf_token) {
      data = jQuery.extend({}, sc);
      data.when = data.when.getTime();
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/emergency_shutoff", data);
    },
    deleteScheduledEnableUpdates: function(sc_id, data_version, csrf_token) {
      return $http.delete(
          `/api/scheduled_changes/emergency_shutoff/${sc_id}?data_version=${data_version}&csrf_token=${encodeURIComponent(csrf_token)}`);
    },
    signoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("emergency_shutoff", sc_id);
      return $http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("emergency_shutoff", sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return $http.delete(url, data);
    }
  };

  return service;
});