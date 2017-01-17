angular.module("app").factory("ProductRequiredSignoffs", function($http, $q) {
  var service = {
    getRequiredSignoffs: function() {
      return $http.get("/api/required_signoffs/product");
    },
    addRequiredSignoff: function(data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.post("/api/required_signoffs/product", data);
    },
  };
  return service;
});
