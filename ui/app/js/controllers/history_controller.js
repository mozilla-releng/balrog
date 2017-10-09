angular
  .module("app")
  .controller("HistoryController", function($scope, $filter, Releases, Rules, History, Page) {
    
    Page.setTitle("History");

    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.maxSize = 10;

    $scope.username_email = "";
    $scope.hs_startDate = "";
    $scope.hs_endDate = "";
    $scope.hs_pr_ch_filter = "All Rules";

    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;
    
    $scope.allHistory = [];
    $scope.rules_revisions = [];

    $scope.pr_ch_options = [];
    $scope.tableResult = true;
    $scope.calendar_is_open = false;

    $scope.loading = false;
    $scope.failed = false;

    $scope.checkBoxes = [];
    var list1 = {
      name: "Rules",
      subs: [
        {
          subname: "Rules",
          id: 1,
          selected: false
        },
        {
          subname: "Scheduled Changes",
          id: 2,
          selected: false
        }
      ]
    };
    var list2 = {
      name: "Releases",
      subs: [
        {
          subname: "Releases",
          id: 1,
          selected: false
        },
        {
          subname: "Scheduled Changes",
          id: 2,
          selected: false
        }
      ]
    };
    var list3 = {
      name: "Permissions",
      subs: [
        {
          subname: "Permissions",
          id: 1,
          selected: false
        },
        {
          subname: "Scheduled Changes",
          id: 2,
          selected: false
        }
      ]
    };
    $scope.checkBoxes.push(list1,list2,list3);

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

    $scope.$watch("add_filter", function(value) {
      $scope.filtering = value.value.split(",");
    });
    $scope.add_filtering_options = [
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
    $scope.add_filter = $scope.add_filtering_options[0];

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
            $scope.hs_pr_ch_filter = "All rules";
            if (
              $scope.pr_ch_options.includes(
                localStorage.getItem("hs_pr_ch_filter")
              )
            ) {
              $scope.pr_ch_filter = localStorage.getItem("hs_pr_ch_filter");
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

    $scope.optionChecked = function(choice) {
      $scope.details = [];
      angular.forEach(choice, function(items) {
        angular.forEach(items.subs, function(value, key) {
          if (items.subs[key].selected) {
            $scope.details.push(items.subs[key].subname);
          }
        });
      });
      if ($scope.details.length > 0){
        $scope.msg = 'Filtering will be done in: ' +$scope.details.toString();
      }
      else{
        sweetAlert(
          "Form submission error",
          "Please check a box",
          "error"
        );
      }
    };

    function isInArray(name,details) {
      for (var i = 0; i < details.length; i++) {
          if (details[i].toLowerCase() === name.toLowerCase()){
            return true;
          }
      }
      return false;
    }

    var newPage;
    function loadHistory(newPage) {
      $scope.loading=true;
      return new Promise(function(resolve, reject) {
        if (isInArray("Rules",$scope.details)){
          History.getRulesHistory($scope.pageSize, newPage)
          .success(function(response) {
            $scope.rules_history_count = response.count;
            $scope.rules_revisions = response.revisions;
            var revisions_arr = [];
            $scope.rules_revisions.forEach(function(revision) {
              if (revision.product) {
                revisions_arr.push(revision);
              }
            });
            resolve(revisions_arr);
          })
          .error(function() {
            console.error(arguments);
            $scope.failed = true;
          })
          .finally(function() {
            $scope.loading = false;
          });
        }
      });
    }

    $scope.searchItem = function() {
      $scope.optionChecked($scope.checkBoxes);
      if($scope.details.length > 0 && $scope.details[0] !== null){
        if ($scope.isShowUsername || $scope.isShowTimestamp || $scope.isShowPrCh) {
          $scope.$watch("currentPage", function(newPage) {
            loadHistory(newPage).then(function(revision) {
              $scope.allHistory = revision;
              if ($scope.username_email !== "") {
                $scope.search = $scope.username_email;
              } else if ($scope.hs_startDate !== "" || $scope.hs_endDate !== "") {
                $scope.search = $filter("dateRangefilter")($scope.allHistory, $scope.hs_startDate , $scope.hs_endDate);
              } else if ($scope.pr_ch_selected[0].toLowerCase() !== "all rules") {
                $scope.search = $scope.hs_pr_ch_filter;
              } else {
                sweetAlert(
                  "Form submission error",
                  "Please enter value in at least one of the field below",
                  "error"
                );
              }
              $scope.$apply();
            });
          });
        } else {
          sweetAlert(
            "Form submission error",
            "There are no search filter fields",
            "error"
          );
        }
      }
    };
  });
