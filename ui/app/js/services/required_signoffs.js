// Inheritance model inspired by:
// http://blog.mgechev.com/2013/12/18/inheritance-services-controllers-in-angularjs/
// http://davidshariff.com/blog/javascript-inheritance-patterns/

var RequiredSignoffBase = (function() {
  var service = {
    getRequiredSignoffs: function() {
      var uri = "/api" + this.base_uri;
      return this.http.get(uri);
    },
    addRequiredSignoff: function(data) {
      var uri = "/api" + this.base_uri;
      return this.http.post(uri, data);
    },
    getScheduledChanges: function() {
      var uri = "/api/scheduled_changes" + this.base_uri;
      return this.http.get(uri);
    },
    addScheduledChange: function(data) {
      var uri = "/api/scheduled_changes" + this.base_uri;
      return this.http.post(uri, data);
    },
  };
  return service;
}());

angular.module("app").factory("ProductRequiredSignoffs", function($http) {
  var service = Object.create(RequiredSignoffBase);
  service.base_uri = "/required_signoffs/product";
  service.http = $http;
  return service;
});

angular.module("app").factory("PermissionsRequiredSignoffs", function($http) {
  var service = Object.create(RequiredSignoffBase);
  service.base_uri = "/required_signoffs/permissions";
  service.http = $http;
  return service;
});
