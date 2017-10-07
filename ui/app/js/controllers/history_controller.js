angular
  .module("app")
  .controller("HistoryController", function(
    $scope,
    Releases,
    Rules,
    History,
    Page
  ) {
    Page.setTitle("History");

    $scope.columnTab = 1;
    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.maxSize = 10;
    $scope.rowtab = "#rulesHistory";
    $scope.filter = [];
    $scope.hs_startDate = "";
    $scope.hs_endDate = "";
    $scope.userInput = {
      username_email: "",
      hs_startDate: "",
      //   hs_date: "",
      hs_pr_ch_filter: "All Rules"
    };
    $scope.search = {};
    $scope.loading = true;
    $scope.failed = false;
    // $scope.rules = [];

    $scope.pr_ch_options = [];

    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;

    $scope.calendar_is_open = false;

    $scope.allHistory = [];
    $scope.rules_revisions = [];

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

    // $scope.allHistory = [
    //   {
    //     changed_by: "Hope",

    //   },
    //   {
    //     changed_by: "Ken",
    //   },
    //   {
    //     changed_by: "Hope",
    //   },
    // ]

    //tabs
    $scope.setColumnTab = function(newTab) {
      $scope.columnTab = newTab;
    };

    $scope.columnTabSet = function(tabNum) {
      return $scope.columnTab === tabNum;
    };

    $scope.tabChange = function(e) {
      if (e.target.nodeName === "A") {
        $scope.rowtab = e.target.getAttribute("href");
        e.preventDefault();
      }
    };

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
        $scope.userInput.username_email = "";
      } else if (value === "timestamp") {
        $scope.isShowTimestamp = true;
      } else if (value === "product_channel") {
        $scope.userInput.hs_pr_ch_filter = "All Rules";
        $scope.isShowPrCh = true;
      }
    };

    //remove filter
    $scope.hideUsername = function() {
      $scope.isShowUsername = $scope.isShowUsername ? false : true;
      $scope.userInput.username_email = "";
    };
    $scope.hideTimestamp = function() {
      $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;
    };
    $scope.hidePrCh = function() {
      $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
    };

    //for product channel filter
    Rules.getRules().success(function(response) {
      $scope.rules = response.rules;
      var pairExists = function(pr, ch) {
        var _rules = $scope.rules.filter(function(rule) {
          return rule.product === pr && rule.channel === ch;
        });
        return _rules.length !== 0;
      };
      Rules.getProducts().success(function(response_prs) {
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
            $scope.userInput.hs_pr_ch_filter = "All rules";
            if (
              $scope.pr_ch_options.includes(
                localStorage.getItem("userInput.hs_pr_ch_filter")
              )
            ) {
              $scope.pr_ch_filter = localStorage.getItem(
                "userInput.hs_pr_ch_filter"
              );
            }
          });
      });
    });
    $scope.pr_ch_selected = [];
    $scope.$watch("userInput.hs_pr_ch_filter", function(value) {
      if (value) {
        localStorage.setItem("userInput.hs_pr_ch_filter", value);
      }
      $scope.pr_ch_selected = value.split(",");
      if ($scope.pr_ch_selected[0].toLowerCase() === "all rules") {
        return true;
      } else {
        $scope.searchItem();
      }
    });
    $scope.searchItem = function() {
      var username_email = $scope.userInput.username_email;
      // var hs_pr_ch_filter = $scope.pr_ch_selected ;
      if (
        $scope.isShowUsername || $scope.isShowTimestamp || $scope.isShowPrCh
      ) {
        if (username_email != "") {
          // $scope.search = moment($scope.userInput.hs_startDate).format("DD/MM/YYYY h:mm:ss a");
          $scope.search = username_email;
          console.log($scope.search);
        } else if ($scope.hs_startDate || $scope.hs_endDate != "") {
          $scope.search = moment($scope.userInput.hs_startDate).format(
            "DD/MM/YYYY h:mm:ss a"
          );
          console.log($scope.search);
        } else if ($scope.pr_ch_selected[0].toLowerCase() != "all rules") {
          console.log("search product channel");
        } else {
          sweetAlert(
            "Form submission error",
            "Please enter value in all field/s or remove unused fields",
            "error"
          );
        }
      } else {
        sweetAlert(
          "Form submission error",
          "There are no search filter fields",
          "error"
        );
      }

      // for (prop in $scope.userInput) {
      //   console.log($scope.userInput.username_email, "prop");
      //   $scope.search[prop] = $scope.userInput[prop];
      // }
    };

    History.getRulesHistory()
      .success(function(response) {
        console.log("response", response);
        $scope.rules_history_count = response.count;

        $scope.rules_revisions = response.revisions;
        $scope.rules_revisions.forEach(function(value, key) {
          if (value.product) {
            $scope.allHistory.push(value);
            // console.log($scope.allHistory,"sfgjhkaldj");
          }
        });
      })
      .error(function() {
        console.error(arguments);
        $scope.failed = true;
      })
      .finally(function() {
        $scope.loading = false;
      });
  });
