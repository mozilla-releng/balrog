angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getrrpHistory: function(checkboxValues, filterParams){
        var url = '/api/rrp/history';
        url += '?rules=' +checkboxValues.rules + '&releases=' +checkboxValues.releases + '&permissions=' +checkboxValues.permissions;
        if (filterParams.changedByValue){
          url += '&changed_by=' + filterParams.changedByValue;
        }
        if (filterParams.startDate && filterParams.endDate){
          url += '&timestamp_from=' + filterParams.startDate + '&timestamp_to=' + filterParams.endDate;
        }
        if (filterParams.product && filterParams.channel){
          url += '&product=' + filterParams.product + '&channel=' + filterParams.channel;
        } else if (filterParams.product){
          url += '&product=' + filterParams.product;
        }
        return $http.get(url) ;
      },

      getscHistory: function(checkboxValues, filterParams) {
        var url = '/api/sc/history';
        url += '?rules_scheduled_change=' +checkboxValues.rules_scheduled_change +
        '&releases_scheduled_change=' +checkboxValues.releases_scheduled_change +
        '&permissions_scheduled_change=' +checkboxValues.permissions_scheduled_change +
        '&permissions_required_signoff_scheduled_change=' +checkboxValues.permissions_required_signoff_scheduled_change +
        '&product_required_signoff_scheduled_change=' +checkboxValues.product_required_signoff_scheduled_change;
        if (filterParams.changedByValue){
          url += '&changed_by=' + filterParams.changedByValue;
        }
        if (filterParams.startDate && filterParams.endDate){
          url += '&timestamp_from=' + filterParams.startDate + '&timestamp_to=' + filterParams.endDate;
        }
        if (filterParams.product && filterParams.channel){
          url += '&product=' + filterParams.product + '&channel=' + filterParams.channel;
        } else if (filterParams.product){
          url += '&product=' + filterParams.product;
        }
        return $http.get(url) ;
      },
      getsignoffHistory: function(checkboxValues, filterParams) {
        var url = '/api/required_signoff/history';
        url += '?permissions_required_signoffs=' +checkboxValues.permissions_required_signoffs +
        '&product_required_signoffs=' +checkboxValues.product_required_signoffs;
        if (filterParams.changedByValue){
          url += '&changed_by=' + filterParams.changedByValue;
        }
        if (filterParams.startDate && filterParams.endDate){
          url += '&timestamp_from=' + filterParams.startDate + '&timestamp_to=' + filterParams.endDate;
        }
        if (filterParams.product && filterParams.channel){
          url += '&product=' + filterParams.product + '&channel=' + filterParams.channel;
        } else if (filterParams.product){
          url += '&product=' + filterParams.product;
        }
        return $http.get(url) ;
      },    
    };
    return service; 
  });
  