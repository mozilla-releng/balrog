angular.module("app").controller('HistoryController',
function($scope, Releases, Page) {
    Page.setTitle('History');
    
    $scope.columnTab = 1;
    $scope.rowtab = "#rulesHistory";
    $scope.filter = [];
    $scope.username = "";
    $scope.timestamp = "";
    $scope.product_channel = "";

    $scope.loading = true;
    $scope.failed = false;
    
    $scope.setColumnTab = function(newTab){
        $scope.columnTab = newTab;
    };

    $scope.columnTabSet = function(tabNum){
        return $scope.columnTab === tabNum;
    };

    $scope.tabChange = function(e){
        if (e.target.nodeName === 'A') {
            $scope.rowtab = e.target.getAttribute("href");
            e.preventDefault();
        }
    };

    $scope.$watch('filtering_str', function(value) {
        $scope.filtering = value.value.split(',');
      });
    $scope.filtering_options = [
        {
        text: "",
        value: "default"
        },
        {
        text: "Username / Email",
        value: "username_email"
        },
        {
        text: "Timestamp",
        value: "timestamp"
        },
        {
        text: "Product/Channel",
        value: "product_channel"
        },
    ];
    $scope.filtering_str = $scope.filtering_options[0];

    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;

    $scope.isField = function(value) {
        if (value === "username_email"){
            $scope.isShowUsername = $scope.isShowUsername ? false : true;
        }
        else if (value === "timestamp"){
            $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;
        }
        else if (value === "product_channel"){
            $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
        }
    };

    $scope.filterSelected = function(value) {
        if (value === "username_email"){
            $scope.isShowUsername = true;
        }
        else if (value === "timestamp"){
            $scope.isShowTimestamp = true;
        }
        else if (value === "product_channel"){
            $scope.isShowPrCh =  true;
        }
    };

    $scope.history = [];
    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;
    
    $scope.hideUsername = function () {
        $scope.isShowUsername = $scope.isShowUsername ? false : true;
    };
    $scope.hideTimestamp = function () {
        $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;
    };
    $scope.hidePrCh = function () {
        $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
    };



    // $scope.histories = [];
    // Releases.getReleases()
    // .success(function(response) {
    //     var releases = response.releases;
    //     releases.forEach(function(release) { 
    //         Releases.getHistory(release.name, $scope.pageSize, 1)
    //         .success(function(response) {
            //    $scope.release_revisions = response.revisions;
            //     $scope.release_history_count = response.count;
    //             // console.log(response.revisions,"response");
    //             // if (response.revisons > 1) {
    //             //     console.log({ name: release.name, releases: response });
    //             // }
    //         })
    //         .error(function() {
        //       console.error(arguments);
        //       $scope.failed = true;
        //     });
    //     })
//         .error(function() {
    //       console.error(arguments);
    //       $scope.failed = true;
    //     })
    //     .finally(function() {
    //       $scope.loading = false;
    //     }); 
    // });
   
        
    function getDummyData() {
        return [
            {
                historyId: 184949,
                object_name: "Tiger Nixon",
                email: "Edinburgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 184949,
                object_name: "Tiger Nixon",
                email: "Edinburgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 184949,
                object_name: "Tiger Nixon",
                email: "Edinburgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 184949,
                object_name: "Tiger Nixon",
                email: "Edinburgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 184945549,
                object_name: "Hope Niefxon",
                email: "hope@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 18494549,
                object_name: "Tiger Nggdggixon",
                email: "Edinbsffurgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 1234949,
                object_name: "Tigesffr Nixon",
                email: "Edinburdfsfsgh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            },
            {
                historyId: 244,
                object_name: "Tigerssfs Nixon",
                email: "Edinburgsfssh@gmail.com",
                start_date: "2011\/04\/25",
                end_date: "2011\/04\/25"
            }

        ];
    };
    $scope.allHistory = getDummyData();
    




});
