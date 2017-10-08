angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getRulesHistory: function(limit, page) {
        return $http.get('/api/history/rules?limit=' + limit + '&page=' + page);
      },
      getReleaseHistory: function() {
        return $http.get('/api/history/release');
      },
    
    };
  
    return service;
  
  });
  