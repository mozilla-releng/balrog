angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getHistory: function(filterParams){
        var url = '/api/' +(filterParams.objectValue) +'/history?';
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
        console.log(url,"ur");
        return $http.get(url) ;
      },
    };
    return service; 
  });
  