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
      dateRangeStart: "",
      dateRangeEnd: "",
      hs_pr_ch_filter: "All Rules"
    };

    $scope.isShowUsername = true;
    $scope.isShowDaterange = true;
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

    $scope.endDateBeforeRender = endDateBeforeRender;
    $scope.endDateOnSetTime = endDateOnSetTime;
    $scope.startDateBeforeRender = startDateBeforeRender;
    $scope.startDateOnSetTime = startDateOnSetTime;

    function startDateOnSetTime() {
      $scope.$broadcast("start-date-changed");
    }
    function endDateOnSetTime() {
      $scope.$broadcast("end-date-changed");
    }

    function startDateBeforeRender($dates) {
      if ($scope.userInput.dateRangeEnd) {
        var activeDate = moment($scope.userInput.dateRangeEnd);

        $dates.filter(function(date) {
            return date.localDateValue() >= activeDate.valueOf();
          }).forEach(function(date) {
            date.selectable = false;
          });
      }
    }

    function endDateBeforeRender($view, $dates) {
      if ($scope.userInput.dateRangeStart) {
        var activeDate = moment($scope.userInput.dateRangeStart)
          .subtract(1, $view)
          .add(1, "minute");

        $dates.filter(function(date) {
            return date.localDateValue() <= activeDate.valueOf();
          }).forEach(function(date) {
            date.selectable = false;
          });
      }
    }

    $scope.getOption = function() {
      var selected = $scope.selected;
      switch (selected) {
        case "username_email":
          $scope.isShowUsername = true;
          break;
        case "daterange":
          $scope.isShowDaterange = true;
          break;
        case "product_channel":
          $scope.hs_pr_ch_filter = "All Rules";
          $scope.isShowPrCh = true;
          break;
      }
      $scope.selected = "";
    };

    $scope.hideUsername = function() {
      $scope.isShowUsername = false;
    };
    $scope.hideDaterange = function() {
      $scope.isShowDaterange = false;
    };
    $scope.hidePrCh = function() {
      $scope.isShowPrCh = false;
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
      $scope.checkedBoxesArr = [];
      angular.forEach(choice, function(value, key) {
        if (choice[key].selected) {
          $scope.checkedBoxesArr.push(choice[key].name);
        }
      });
      if ($scope.checkedBoxesArr.length > 0) {
        $scope.msg = "Filtering will be done in: " + $scope.checkedBoxesArr.toString();
      } else {
        sweetAlert("Form submission error", "Please check a box", "error");
      }
    };

    function isInArray(name, checkedBoxesArr) {
      for (var i = 0; i < checkedBoxesArr.length; i++) {
        if (checkedBoxesArr[i].toLowerCase() === name.toLowerCase()) {
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

    var promises = [];
    function rulesHistory() {
      switch ($scope.tab) {
        case 1:
          console.log("calling rulesendpoint");
          promises.push(
            History.getRulesHistory($scope.pageSize)
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
          break;
        case 2:
          console.log("calling rules scheduled changes endpoint");
          break;
        case 3:
          console.log("calling rules required signoff endpoint");
          break;
      }
    }

    function releasesHistory() {
      switch ($scope.tab) {
        case 1:
          console.log("calling release endpoint");
          promises.push(
            History.getReleaseHistory($scope.pageSize)
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
          break;
        case 2:
          console.log("calling release scheduled changes endpoint");
          break;
        case 3:
          console.log("calling releases required signoff endpoint");
          break;
      }
    }

    function loadHistory() {
      $scope.loading = true;
      return new Promise(function(resolve, reject) {
        if (isInArray("Rules", $scope.checkedBoxesArr)) {
          rulesHistory();
        }
        if (isInArray("Releases", $scope.checkedBoxesArr)) {
          releasesHistory();
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
      if ($scope.checkedBoxesArr.length > 0 && $scope.checkedBoxesArr[0] !== null) {
        if ($scope.isShowUsername || $scope.isShowTimestamp || $scope.isShowPrCh) {
          loadHistory().then(function(data) {
            $scope.allHistory = data;
            $scope.$apply(function() {
              if ($scope.userInput.username_email !== "") {
                var changedByArr = [];
                var searchResult = [];
                $scope.userInput.username_email.forEach(function(changedBy) {
                  if (changedByArr.indexOf(changedBy.name) == -1) {
                    changedByArr.push(changedBy.name);
                    changedByArr.forEach(function(name) {
                      if (searchResult.indexOf(name) == -1) {
                        $scope.search = $filter("filter")(
                          $scope.allHistory,
                          name
                        );
                      }
                    });
                  }
                });
              } 
              if ($scope.userInput.dateRangeStart !== "" ||$scope.userInput.dateRangeEnd !== "") {
                $scope.search = $filter("dateRangefilter")($scope.allHistory,$scope.userInput.dateRangeStart,$scope.userInput.dateRangeEnd);
              } 
              if ($scope.pr_ch_selected[0].toLowerCase() !== "all rules") {
                $scope.search = $filter("filter")($scope.allHistory,$scope.userInput.hs_pr_ch_filter);
              } 
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
