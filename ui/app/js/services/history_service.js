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

      getScheduedReleaseDiff: function(change_id) {
        var url = '/api/history/diff/sc/release/' + change_id;
        return $http({
          url: url,
          method: 'GET',
          transformResponse: function(value) {
            return value;
          }
        });
      },
      };
    return service; 
  });
  