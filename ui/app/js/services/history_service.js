angular.module("app").factory('History', function($http, $q, ScheduledChanges, Helpers) {
    var service = {
      getHistory: function(filterParams, page){
        var url = '/api/' +(filterParams.objectValue) +'/history?';
        url += 'page=' + page;
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
    };
    return service; 
  });
  