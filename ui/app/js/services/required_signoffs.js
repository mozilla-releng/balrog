// Inheritance model inspired by:
// http://blog.mgechev.com/2013/12/18/inheritance-services-controllers-in-angularjs/
// http://davidshariff.com/blog/javascript-inheritance-patterns/

var RequiredSignoffBase = (function() {
  var service = {
    getRequiredSignoffs: function() {
      var url = "/api" + this.base_url;
      return this.http.get(url);
    },
    addRequiredSignoff: function(data) {
      var url = "/api" + this.base_url;
      return this.http.post(url, data);
    },
    getScheduledChanges: function() {
      var url = "/api/scheduled_changes" + this.base_url;
      return this.http.get(url);
    },
    addScheduledChange: function(data) {
      var url = "/api/scheduled_changes" + this.base_url;
      return this.http.post(url, data);
    },
    updateScheduledChange: function(sc_id, data) {
      var url = "/api/scheduled_changes" + this.base_url + "/" + sc_id;
      return this.http.post(url, data);
    },
    deleteScheduledChange: function(sc_id, data) {
      var url = "/api/scheduled_changes" + this.base_url + "/" + sc_id;
      url += "?data_version=" + data["sc_data_version"];
      url += "&csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return this.http.delete(url);
    },
  };
  return service;
}());

angular.module("app").factory("ProductRequiredSignoffs", function($http) {
  var service = Object.create(RequiredSignoffBase);
  service.base_url = "/required_signoffs/product";
  service.http = $http;
  return service;
});

angular.module("app").factory("PermissionsRequiredSignoffs", function($http) {
  var service = Object.create(RequiredSignoffBase);
  service.base_url = "/required_signoffs/permissions";
  service.http = $http;
  return service;
});
