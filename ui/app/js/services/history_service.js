angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getRulesHistory: function() {
        return $http.get('/api/history/rules');
      },
      getReleaseHistory: function() {
        return $http.get('/api/history/releases');
      },
      getPermissionsHistory: function() {
        return $http.get('/api/history/permissions');
      },
      getScRulesHistory: function() {
        return $http.get('/api/history/scheduled_changes/rules');
      },
      getScReleasesHistory: function() {
        return $http.get('/api/history/scheduled_changes/releases');
      },
      getProductRsHistory: function() {
        return $http.get('/api/history/product_required_signoffs');
      },
      getPermissionRsHistory: function() {
        return $http.get('/api/history/permissions_required_signoffs');
      },
      getrrpHistory: function(checkboxValues, changed_by) {
        console.log(checkboxValues,"checkboxValues");
        var url = '/api/rrp/histories';
        url += '?rules=' +checkboxValues.rules + '&releases=' +checkboxValues.releases + '&permissions=' +checkboxValues.permissions;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },
    
    };
  
    return service;
  
  });
  