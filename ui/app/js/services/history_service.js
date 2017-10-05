angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getRulesHistory: function() {
        return $http.get('/api/history/rules');
      },
      getReleaseHistory: function() {
        return $http.get('/api/history/release');
      },
    
    };
  
    return service;
  
  });
  