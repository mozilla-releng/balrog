// angular.module("app").config(function($httpProvider){
//   $httpProvider.defaults.headers.put['Content-Type'] = 'multipart/form-data';
// });

angular.module("app").factory('RulesService', function($http) {
  // these routes map to stubbed API endpoints in config/server.js
  // var csrf_token = null;
  var service = {
    getRules: function() {
      return $http.get('/api/rules');
    },
    getRule: function(id) {
      return $http.get('/api/rules/' + id);
    },
    updateRule: function(id, data, csrf_token) {
      data.csrf_token = csrf_token;
      return $http.put('/api/rules/' + id, data);
    },
    deleteRule: function(id, data, csrf_token) {
      // data.csrf_token = csrf_token;
      var url = '/api/rules/' + id;
      url += '?data_version=' + data.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
  };
  return service;

});
