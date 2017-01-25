// Inheritance model inspired by:
// http://blog.mgechev.com/2013/12/18/inheritance-services-controllers-in-angularjs/
// http://davidshariff.com/blog/javascript-inheritance-patterns/

var RequiredSignoffBase = (function() {
  var service = {
    getRequiredSignoffs: function() {
      var uri = this.base_uri;
      return this.http.get(uri);
    },
    addRequiredSignoff: function(data) {
      var uri = this.base_uri;
      return this.http.post(uri, data);
    },
  };
  return service;
}());

angular.module("app").factory("ProductRequiredSignoffs", function($http) {
  var service = Object.create(RequiredSignoffBase);
  service.base_uri = "/api/required_signoffs/product";
  service.http = $http;
  return service;
});
