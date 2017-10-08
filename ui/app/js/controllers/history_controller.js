angular
  .module("app")
  .controller("HistoryController", function(
    $scope,
    $filter,
    Releases,
    Rules,
    History,
    Page
  ) {
    Page.setTitle("History");
    $scope.rulesCheckbox = false;

    $scope.columnTab = 1;
    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.maxSize = 10;
    $scope.hs_startDate = "";
    $scope.hs_endDate = "";
    $scope.filter = [];
    $scope.username_email = "";
    $scope.hs_pr_ch_filter = "All Rules";

    $scope.loading = true;
    $scope.failed = false;

    $scope.pr_ch_options = [];

    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;

    $scope.tableResult = true;

    $scope.calendar_is_open = false;

    $scope.allHistory = [];
    
    $scope.rules_revisions = [];

    var newArr = [];
    var list1 = {
      name: "Rules",
      subs: [{
        sub: "Rules",
        id: 1,
        selected: false
      }, {
        sub: "Scheduled Changes",
        id: 2,
        selected: false
      }],
    };
    var list2 = {
      name: "Releases",
      subs: [{
        sub: "Releases",
        id: 1,
        selected: false
      }, {
        sub: "Scheduled Changes",
        id: 2,
        selected: false
      }],
    };
    var list3 = {
      name: "Permissions",
      subs: [{
        sub: "Permissions",
        id: 1,
        selected: false
      }, {
        sub: "Scheduled Changes",
        id: 2,
        selected: false
      }],
    };
    newArr.push(list1);
    newArr.push(list2);
    newArr.push(list3);
  
    $scope.itemDisplayed = newArr;
  
  
    $scope.optionToggled = function(item, subs) {
      var trues = $filter("filter")($scope.itemDisplayed, {
          value: true
      });
      return trues.length;
  }
    $scope.setWhen = function(newDate) {
      $scope.calendar_is_open = false;
      if (newDate >= new Date()) {
        $scope.date_error = ["Date cannot be ahead of the present date"];
        $scope.hs_startDate = null;
        $scope.hs_endDate = null;
      } else {
        $scope.date_error = null;
      }
    };

    // $scope.search = [
    //   {
    //     changed_by: "Hope",
    //        timestamp: "20/09/2017"
    //   },
    //   {
    //     changed_by: "Ken",
    // timestamp: "20/09/2017"
    //   },
    //   {
    //     changed_by: "Hope",
    // timestamp: "20/06/2017"
    //   },
    // ]

    //add filter options
    $scope.$watch("filtering_str", function(value) {
      $scope.filtering = value.value.split(",");
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
      }
    ];
    $scope.filtering_str = $scope.filtering_options[0];

    $scope.filterSelected = function(value) {
      if (value === "username_email") {
        $scope.isShowUsername = true;
        $scope.username_email = "";
      } else if (value === "timestamp") {
        $scope.isShowTimestamp = true;
      } else if (value === "product_channel") {
        $scope.hs_pr_ch_filter = "All Rules";
        $scope.isShowPrCh = true;
      }
    };

    //remove filter
    $scope.hideUsername = function() {
      $scope.isShowUsername = $scope.isShowUsername ? false : true;
      $scope.username_email = "";
    };
    $scope.hideTimestamp = function() {
      $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;
    };
    $scope.hidePrCh = function() {
      $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
    };

    //for product channel filter
    Rules.getRules()
    .success(function(response) {
      $scope.rules = response.rules;
      // console.log($scope.rules);
      var pairExists = function(pr, ch) {
        var _rules = $scope.rules.filter(function(rule) {
          return rule.product === pr && rule.channel === ch;
        });
        return _rules.length !== 0;
      };
      Rules.getProducts()
      .success(function(response_prs) {
        Rules.getChannels()
          .success(function(response_chs) {
            response_prs.product.forEach(function(pr) {
              $scope.pr_ch_options.push(pr);
              response_chs.channel.forEach(function(ch) {
                if (ch.indexOf("*") === -1 && pairExists(pr, ch)) {
                  var pr_ch_pair = pr.concat(",").concat(ch);
                  $scope.pr_ch_options.push(pr_ch_pair);
                }
              });
            });
          })
          .finally(function() {
            $scope.pr_ch_options.sort().unshift("All rules");
            $scope.hs_pr_ch_filter = "All rules";
            if (
              $scope.pr_ch_options.includes(
                localStorage.getItem("hs_pr_ch_filter")
              )
            ) {
              $scope.pr_ch_filter = localStorage.getItem(
                "hs_pr_ch_filter"
              );
            }
          });
      });
    });
    $scope.pr_ch_selected = [];
    $scope.$watch("hs_pr_ch_filter", function(value) {
      if (value) {
        localStorage.setItem("hs_pr_ch_filter", value);
      }
      $scope.pr_ch_selected = value.split(",");
      if ($scope.pr_ch_selected[0].toLowerCase() === "all rules") {
        return true;
      } else {
        $scope.searchItem();
      }
    });
    
    var newPage;
    function loadHistory(newPage) {
      return new Promise(function(resolve, reject){
        History.getRulesHistory($scope.pageSize, newPage)
        .success(function(response) {
          console.log(response,"response");
          $scope.rules_history_count = response.count;
          $scope.rules_revisions = response.revisions;
          var test= [];
          $scope.rules_revisions.forEach(function(revision) {
            console.log(revision,"revision");
            if (revision.product) {
             test.push(revision);
              // resolve(revision);
              // $scope.allHistory.push(revision);
            }
          });
          resolve(test);
        })
        .error(function() {
          console.error(arguments);
          $scope.failed = true;
        })
        .finally(function() {
          $scope.loading = false;
        });
      })
      
    }

    $scope.searchItem = function() {
      console.log($scope.allHistory,"historyif")
      if ($scope.isShowUsername  || $scope.isShowTimestamp || $scope.isShowPrCh) {
        $scope.$watch("currentPage", function(newPage) {
          loadHistory(newPage).then(function(revision){
            $scope.allHistory = revision;
            if ($scope.username_email !== "") {
              $scope.search = $scope.username_email;
            } else if ($scope.hs_startDate !== "" || $scope.hs_endDate !== "") {
              $scope.search = $filter("dateRangefilter")($scope.allHistory, $scope.hs_startDate , $scope.hs_endDate);
              console.log($scope.search,"search")
            } else if ($scope.pr_ch_selected[0].toLowerCase() !== "all rules") {
              $scope.search = $scope.hs_pr_ch_filter;
            } else {
              sweetAlert(
                "Form submission error",
                "Please enter value in all field/s or remove unused fields",
                "error"
              );
            }
            $scope.$apply();
          })
        });
        
      } else {
        sweetAlert(
          "Form submission error",
          "There are no search filter fields",
          "error"
        );
      }
      // $scope.$watch("currentPage", function(newPage) {
      //       loadHistory(newPage);
      //     });    
    };
    
  });
