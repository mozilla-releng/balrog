
angular.module("app").filter('dateRangefilter', function($filter) {
    return function(items, start_date, end_date) {
        var hs_startDate = new Date(start_date);
        var hs_endDate = new Date(end_date);
        // console.log(hs_startDate, "start"); 
        // console.log(hs_endDate,"end"); 
        return $filter('filter')(items, function(item) {
            var date = new Date(item.timestamp);
            // console.log(date,"date"); 
            return date >= hs_startDate && date <= hs_endDate;
         });
    }
});
