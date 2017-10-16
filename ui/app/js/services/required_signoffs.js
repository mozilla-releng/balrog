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
    /**
     * Convert a list of {role, signoffs_required} objects into a
     * Map-like object that is easy to deal with in templates even
     * though we can't actually use Map.
     *
     * Returns {length, roles}, where roles is an object with keys
     * being role names and values being the number of signoffs
     * required, and length is the number of keys in roles.
     *
     * FIXME: Not actually a Map
     */
    convertToMap: function(signoffRequirements) {
      var merged = {};
      signoffRequirements.map(function(requirement) {
        if (!merged[requirement.role] || merged[requirement.role] < requirement.signoffs_required) {
          merged[requirement.role] = requirement.signoffs_required;
        }
      });
      return {length: Object.keys(merged).length, roles: merged};

    }
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
