angular.module("app").factory('RulesService', function($http) {
  // these routes map to stubbed API endpoints in config/server.js
  return {
    getRules: function() {
      return $http.get('/api/rules');
    },
    getRule: function(id) {
      return $http.get('/api/rules/' + id);
    }
  };
});
