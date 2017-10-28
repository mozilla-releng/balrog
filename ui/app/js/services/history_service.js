angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getHistory: function(filterParams){
        var url = '/api/history?releases=1';
        if (filterParams.checkboxValue){
          angular.forEach(filterParams.checkboxValue, function(value,key) {
            if (value === 1) {
              url += `&${key}=`+ value;
            }
          })
        }
        if (filterParams.changedByValue){
          url += '&changed_by=' + filterParams.changedByValue;
        }
        if (filterParams.startDate || filterParams.endDate){
            url += '&timestamp_from=' + filterParams.startDate+ '&timestamp_to=' + filterParams.endDate;
          }
        if (filterParams.product && filterParams.channel){
          url += '&product=' + filterParams.product + '&channel=' + filterParams.channel;
        } else if (filterParams.product){
          url += '&product=' + filterParams.product;
        }     
        return $http.get(url) ;
      },
    }
    return service; 
  });
  