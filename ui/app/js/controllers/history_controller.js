angular
  .module("app")
  .controller("HistoryController", function(
    $scope,
    $q,
    $filter,
    Releases,
    Rules,
    History,
    Page
  ) {
    Page.setTitle("History");

    $scope.currentPage = 1;
    $scope.pageSize = 60;
    $scope.maxSize = 10;

    $scope.userInput = {
      username_email: [],
      hs_startDate: "",
      hs_endDate: "",
      hs_pr_ch_filter: "All Rules"
    };

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
    $scope.tab = 1;

    $scope.setTab = function(newTab) {
      $scope.tab = newTab;
    };

    $scope.isSet = function(tabNum) {
      return $scope.tab === tabNum;
    };

    $scope.checkBoxes = [
      {
        id: 1,
        name: "Rules",
        selected: false
      },
      {
        id: 2,
        name: "Releases",
        selected: false
      },
      {
        id: 3,
        name: "Permissions",
        selected: false
      }
    ];

    $scope.addUsernameEmail = function() {
      $scope.userInput.username_email.push({ name: $scope.usernameEmailText });
      console.log($scope.userInput.username_email, "usericvvnput");
      $scope.usernameEmailText = "";
    };

    $scope.deleteUsernameEmail = function(key) {
      if (
        $scope.userInput.username_email.length > 0 &&
        $scope.usernameEmailText.length == 0 &&
        key === undefined
      ) {
        $scope.userInput.username_email.pop();
      } else if (key != undefined) {
        $scope.userInput.username_email.splice(key, 1);
      }
    };

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
      $scope.userInput.username_email = "";
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

    $scope.optionChecked = function(choice) {
      $scope.details = [];
      angular.forEach(choice, function(value, key) {
        if (choice[key].selected) {
          $scope.details.push(choice[key].name);
        }
      });
      if ($scope.details.length > 0) {
        $scope.msg = "Filtering will be done in: " + $scope.details.toString();
      } else {
        sweetAlert("Form submission error", "Please check a box", "error");
      }
    };

    function isInArray(name, details) {
      for (var i = 0; i < details.length; i++) {
        if (details[i].toLowerCase() === name.toLowerCase()) {
          return true;
        }
      }
      return false;
    }

    $scope.processResponse = function(response) {
      $scope.history_count = response.count;
      $scope.revisions = response.revisions;
      var revisions_arr = [];
      $scope.revisions.forEach(function(revision) {
        revisions_arr.push(revision);
      });
    };

    var newPage;
    function loadHistory(newPage) {
      var promises = [];
      $scope.loading = true;
      return new Promise(function(resolve, reject) {
        if (isInArray("Rules", $scope.details)) {
          promises.push(
            History.getRulesHistory($scope.pageSize, newPage)
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
        }
        if (isInArray("Releases", $scope.details)) {
          promises.push(
            History.getReleaseHistory($scope.pageSize, newPage)
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
        }

        $q.all(promises).then(function(response) {
          $scope.promiseResult = response;
          var promiseResultArr = [];
          $scope.promiseResult.forEach(function(arrList) {
            var history_arr_list_data = arrList.data;
            history_arr_list_data.revisions.forEach(function(data) {
              promiseResultArr.push(data);
            });
          });
          resolve(promiseResultArr);
          $scope.loading = false;
        });
      });
    }

    $scope.searchItem = function() {
      $scope.optionChecked($scope.checkBoxes);
      if ($scope.details.length > 0 && $scope.details[0] !== null) {
        if (
          $scope.isShowUsername || $scope.isShowTimestamp || $scope.isShowPrCh
        ) {
          $scope.$watch("currentPage", function(newPage) {
            loadHistory(newPage).then(function(data) {
              $scope.allHistory = data;
              $scope.$apply(function() {
                if ($scope.userInput.username_email !== "") {
                  var changedByArr = [];
                  var searchResult = [];
                  $scope.userInput.username_email.forEach(function(changedBy) {
                    if (changedByArr.indexOf(changedBy.name) == -1) {
                      changedByArr.push(changedBy.name);
                      console.log(changedByArr, "changedByaaArr");
                      changedByArr.forEach(function(name) {
                        if (searchResult.indexOf(name) == -1) {
                          $scope.search = $filter("filter")(
                            $scope.allHistory,name);
                        }
                      });
                    }
                  });
                }
                if (
                  $scope.userInput.hs_startDate !== "" ||
                  $scope.userInput.hs_endDate !== ""
                ) {
                  $scope.search = $filter("dateRangefilter")(
                    $scope.allHistory,
                    $scope.userInput.hs_startDate,
                    $scope.userInput.hs_endDate
                  );
                  console.log($scope.search, "search right");
                }
                if ($scope.pr_ch_selected[0].toLowerCase() !== "all rules") {
                  $scope.search = $filter("filter")(
                    $scope.allHistory,
                    $scope.userInput.hs_pr_ch_filter
                  );
                  console.log($scope.search, "search");
                }
              });
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
