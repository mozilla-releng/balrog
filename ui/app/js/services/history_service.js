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
        url += '?rules_scheduled_change=' +checkboxValues.rules_scheduled_change +
        '&releases_scheduled_change=' +checkboxValues.releases_scheduled_change +
        '&permissions_scheduled_change=' +checkboxValues.permissions_scheduled_change +
        '&permissions_required_signoff_scheduled_change=' +checkboxValues.permissions_required_signoff_scheduled_change +
        '&product_required_signoff_scheduled_change=' +checkboxValues.product_required_signoff_scheduled_change;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },
      getsignoffHistory: function(checkboxValues, changed_by) {
        console.log(checkboxValues,"checkboxValues");
        var url = '/api/required_signoff/history';
        url += '?permissions_required_signoffs=' +checkboxValues.permissions_required_signoffs +
        '&product_required_signoffs=' +checkboxValues.product_required_signoffs;
        url += '&changed_by=' + changed_by;
        return $http.get(url) ;
      },    
    };
    return service; 
  });
  