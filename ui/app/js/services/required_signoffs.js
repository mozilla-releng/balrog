// Inheritance model inspired by:
// http://blog.mgechev.com/2013/12/18/inheritance-services-controllers-in-angularjs/
// http://davidshariff.com/blog/javascript-inheritance-patterns/

var RequiredSignoffBase = (function() {
  var service = {
    getRequiredSignoffs: function() {
      var url = "/api/" + this.object_name;
      return this.http.get(url);
    },
    addRequiredSignoff: function(data) {
      data = this.Helpers.replaceEmptyStrings(data);
      var url = "/api/" + this.object_name;
      return this.http.post(url, data);
    },
    getScheduledChanges: function() {
      var url = "/api/scheduled_changes/" + this.object_name;
      return this.http.get(url);
    },
    addScheduledChange: function(data) {
      data = this.Helpers.replaceEmptyStrings(data);
      var url = "/api/scheduled_changes/" + this.object_name;
      return this.http.post(url, data);
    },
    updateScheduledChange: function(sc_id, data) {
      data = this.Helpers.replaceEmptyStrings(data);
      var url = "/api/scheduled_changes/" + this.object_name + "/" + sc_id;
      return this.http.post(url, data);
    },
    deleteScheduledChange: function(sc_id, data) {
      var url = "/api/scheduled_changes/" + this.object_name + "/" + sc_id;
      url += "?data_version=" + data["sc_data_version"];
      url += "&csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return this.http.delete(url);
    },
    signoffOnScheduledChange: function(sc_id, data) {
      var url = this.ScheduledChanges.signoffsUrl(this.object_name, sc_id);
      return this.http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = this.ScheduledChanges.signoffsUrl(this.object_name, sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return this.http.delete(url, data);
    },
  };
  return service;
}());

angular.module("app").factory("ProductRequiredSignoffs", function($http, ScheduledChanges, Helpers) {
  var service = Object.create(RequiredSignoffBase);
  service.object_name = "required_signoffs/product";
  service.http = $http;
  service.ScheduledChanges = ScheduledChanges;
  service.Helpers = Helpers;
  return service;
});

angular.module("app").factory("PermissionsRequiredSignoffs", function($http, ScheduledChanges, Helpers) {
  var service = Object.create(RequiredSignoffBase);
  service.object_name = "required_signoffs/permissions";
  service.http = $http;
  service.ScheduledChanges = ScheduledChanges;
  service.Helpers = Helpers;
  return service;
});
