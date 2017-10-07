
angular.module("app").filter('dateRangefilter', function($filter) {
    return function(items, start_date, end_date) {
        var hs_startDate = moment(start_date).format("DD/MM/YYYY");
        var hs_endDate = moment(end_date).format("DD/MM/YYYY");
        console.log(hs_startDate, "start"); 
        console.log(hs_endDate,"end"); 
        return $filter('filter')(items, function(item) {
            var date = moment(item.timestamp).format("DD/MM/YYYY");
            console.log(date,"date"); 
            return date >= hs_startDate && date <= hs_endDate;
         });
    }
});

