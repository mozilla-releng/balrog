angular.module("app").factory("PermissionsRequiredSignoffs", function($http, $q) {
  var service = {
    getRequiredSignoffs: function() {
      return $http.get("/api/required_signoffs/permissions");
    },
    addRequiredSignoff: function(data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.post("/api/required_signoffs/permissions", data);
    },
  };
  return service;
});
