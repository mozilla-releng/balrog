angular.module('app').factory('EmergencyShutoffs', function($http, ScheduledChanges) {
  var service = {
    get: function() {
      return $http.get('/api/emergency_shutoff');
    },
    create: function(product, channel, csrf_token) {
      data = {'product': product, 'channel': channel, 'csrf_token': csrf_token};
      return $http.post('/api/emergency_shutoff', data);
    },
    delete: function(product, channel, data_version, csrf_token) {
      url = '/api/emergency_shutoff/' + product + '/' + channel + '?data_version=' + data_version + '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    scheduledChanges: function() {
      return $http.get('/api/scheduled_changes/emergency_shutoff');
    },
    scheduleEnableUpdates: function(shutoff, csrf_token) {
      when = new Date();
      when.setSeconds(when.getSeconds() + 10);

      data = angular.copy(shutoff);
      data.change_type = 'delete';
      data.when = when.getTime();
      data.csrf_token = csrf_token;

      return $http.post("/api/scheduled_changes/emergency_shutoff", data);
    },
    deleteScheduledEnableUpdates: function(sc_id, data_version, csrf_token) {
      url = '/api/scheduled_changes/emergency_shutoff/' + sc_id + '?data_version=' + data_version + '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    signoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("emergency_shutoff", sc_id);
      return $http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("emergency_shutoff", sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return $http.delete(url, data);
    },
    shutoffProductSignoffsRequired: function(shutoff, signoffs_requirements) {
      return signoffs_requirements.find(function(required_signoff) {
        return required_signoff.product === shutoff.product && required_signoff.channel === shutoff.channel;
      });
    },
    shutoffScheduledEnableChange: function(shutoff, scheduled_changes) {
      return scheduled_changes.find(function(sc) {
        return sc.product === shutoff.product && sc.channel === shutoff.channel;
      });
    }
  };

  return service;
});