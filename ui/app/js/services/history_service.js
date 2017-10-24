angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getrrpHistory: function(checkboxValues, changed_by) {
        console.log(checkboxValues,"checkboxValues");
        var url = '/api/rrp/history';
        url += '?rules=' +checkboxValues.rules + '&releases=' +checkboxValues.releases + '&permissions=' +checkboxValues.permissions;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },
      getscHistory: function(checkboxValues, changed_by) {
        console.log(checkboxValues,"checkboxValues");
        var url = '/api/sc/history';
        url += '?rules=' +checkboxValues.rules + '&releases=' +checkboxValues.releases + '&permissions=' +checkboxValues.permissions;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },
      getsignoffHistory: function(checkboxValues, changed_by) {
        console.log(checkboxValues,"checkboxValues");
        var url = '/api/required_signoff/history';
        url += '?rules=' +checkboxValues.rules + '&releases=' +checkboxValues.releases + '&permissions=' +checkboxValues.permissions;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },    
    };
    return service; 
  });
  