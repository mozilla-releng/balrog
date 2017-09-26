angular.module("app").controller('HistoryController',
function($scope, Releases, Rules, Page) {
    Page.setTitle('History');
    
    $scope.columnTab = 1;
    $scope.rowtab = "#rulesHistory";
    $scope.filter = [];
    $scope.username_email = "";
    $scope.hs_pr_ch_filter = "All Rules";

    $scope.loading = true;
    $scope.failed = false;

    $scope.pr_ch_options = [];
    $scope.rules = [];
    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;
    $scope.calendar_is_open = false;
    $scope.hs_startDate = "";
    $scope.hs_endDate = "";

    $scope.setWhen = function(newDate) {
        $scope.calendar_is_open = false;
        if (newDate >= new Date()) {
          $scope.date_error = ["Date cannot be ahead of the present date"];
          $scope.hs_startDate = null;
          $scope.hs_endDate = null;
        }
        else {
          $scope.date_error = null;
        }
      };


    //tabs
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

    //add filter options
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

    $scope.filterSelected = function(value) {
        if (value === "username_email"){
            $scope.isShowUsername = true;
            $scope.username_email = "";
        }
        else if (value === "timestamp"){
            $scope.isShowTimestamp = true;
        }
        else if (value === "product_channel"){
            $scope.hs_pr_ch_filter = "All Rules";
            $scope.isShowPrCh =  true;
        }
    };

    //remove filter 
    $scope.hideUsername = function () {
        $scope.isShowUsername = $scope.isShowUsername ? false : true;
        $scope.username_email = "";
    };
    $scope.hideTimestamp = function () {
        $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;

    };
    $scope.hidePrCh = function () {
        $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
    };

    //for product channel filter
    Rules.getRules()
    .success(function(response) {
        $scope.rules = response.rules;
      var pairExists = function(pr, ch) {
        var _rules = $scope.rules.filter(function(rule) {
          return rule.product === pr && rule.channel === ch;
        });
        return _rules.length !== 0;
      };
      Rules.getProducts().success(function(response_prs) {
        Rules.getChannels().success(function(response_chs) {
          response_prs.product.forEach(function(pr) {
            $scope.pr_ch_options.push(pr);
            response_chs.channel.forEach(function(ch) {
              if (ch.indexOf("*") === -1 && pairExists(pr, ch)){
                var pr_ch_pair = pr.concat(",").concat(ch);
                $scope.pr_ch_options.push(pr_ch_pair);
              }
            });
          });
        })
        .finally(function() {
          $scope.pr_ch_options.sort().unshift("All rules");
          $scope.hs_pr_ch_filter = "All rules";
          if ($scope.pr_ch_options.includes(localStorage.getItem('hs_pr_ch_filter'))){
            $scope.pr_ch_filter = localStorage.getItem('hs_pr_ch_filter');
          }
        });
      });
    });

    $scope.$watch('hs_pr_ch_filter', function(value) {
        if (value) {
          localStorage.setItem("hs_pr_ch_filter", value);
        }
        $scope.pr_ch_selected = value.split(',');
      });



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
   
    //dummy data    
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
    }
    $scope.allHistory = getDummyData();
    




});
