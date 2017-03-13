angular.module("app").factory('ScheduledChanges', function() {
  var service = {
    signoffsUrl: function(object_name, sc_id) {
      return "/api/scheduled_changes/" + object_name + "/" + sc_id + "/signoffs";
    },
  };
  return service;
});
