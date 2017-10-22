angular
  .module("app")
  .controller("HistoryController", function($scope, $q, $filter, Releases, Rules, History, Page) {
    
    Page.setTitle("History");

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
    $scope.pr_ch_options = [];
    $scope.tableResult = true;
    $scope.calendar_is_open = false;
    $scope.loading = false;
    $scope.failed = false;
    $scope.tab = 1;
    $scope.rprfilter = true;

    // Setting tabs
    $scope.setTab = function(newTab) {
      $scope.tab = newTab;
      if ($scope.tab === 1 || $scope.tab === 2) {
        $scope.rprfilter = true;
        $scope.so_filter = false;
      } else if ($scope.tab === 3){
        $scope.rprfilter = false;
        $scope.so_filter = true;
      }
    };

    $scope.isSet = function(tabNum) {
      return $scope.tab === tabNum;
    };

    // Checkboxes start
    $scope.checkBoxes = [
      {
        id: 1,
        name: "rules",
        value: "Rules",
        selected: false
      },
      {
        id: 2,
        name: "releases",
        value: "Releases",
        selected: false
      },
      {
        id: 3,
        name: "permissions",
        value: "Permissions",
        selected: false
      }
    ];

    $scope.so_checkBoxes = [
      {
        id: 1,
        name: "product_signoffs",
        value: "Product Signoffs",
        selected: false
      },
      {
        id: 2,
        name: "permissions_signoffs",
        value: "Permissions Signoffs",
        selected: false
      }
    ];

    function optionChecked (choice) {
      $scope.checkedBoxesArr = {rules: 0, releases:0, permissions:0 };
      angular.forEach(choice, function(value, key) {
        if (choice[key].selected) {
          $scope.checkedBoxesArr[choice[key].name] = 1;   
          $scope.msg = "Filtering will be done in: " + $scope.checkedBoxesArr[choice[key].name];  
        }
        else{
          $scope.checkedBoxesArr[choice[key].name] = 0;
          // sweetAlert("Form submission error", "Please check a box", "error");
        }   
      });
      return $scope.checkedBoxesArr;
    };

    // Check if the value checked is in the checkbox array
    // function isInArray(name, checkedBoxesArr) {
    //   for (var i = 0; i < checkedBoxesArr.length; i++) {
    //     if (checkedBoxesArr[i].toLowerCase() === name.toLowerCase()) {
    //       return true;
    //     }
    //   }
    //   return false;
    // }
    //---checkbox ends


    //Add username or email tag into the username/email input field 
    $scope.addUsernameEmail = function() {
      $scope.userInput.username_email.push({ name: $scope.usernameEmailText });
      $scope.usernameEmailText = "";
    };

    //Delete username or email tag from the username/email input field 
    $scope.deleteUsernameEmail = function(key) {
      if ($scope.userInput.username_email.length > 0 && $scope.usernameEmailText.length === 0 &&
        key === undefined) {
        $scope.userInput.username_email.pop();
      } else if (key !== undefined) {
        $scope.userInput.username_email.splice(key, 1);
      }
    };

    //Date range functions- To disable dates before start date
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
    $scope.endDateBeforeRender = endDateBeforeRender;
    $scope.endDateOnSetTime = endDateOnSetTime;
    $scope.startDateBeforeRender = startDateBeforeRender;
    $scope.startDateOnSetTime = startDateOnSetTime;
    //-- Date range ends

    //Product/ Channel  filter
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
        $scope.searchHistory();
      }
    });
    //Product/channel filter ends

    //To add and remove filter fields
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
    //End add and remove filter fields
    
    $scope.processResponse = function(response) {
      $scope.history_count = response.count;
      $scope.revisions = response.revisions;
      var revisions_arr = [];
      $scope.revisions.forEach(function(revision) {
        revisions_arr.push(revision);
      });
    };

    var promises = [];
    var sc_promises = [];
    //To call all rules history and sc_rules history endpoints depending on the tab selected
    function rulesHistory() {
      switch ($scope.tab) {
        case 1:
          promises.push(
            History.getRulesHistory()
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
        sc_promises.push(
            History.getScRulesHistory()
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
          break;
      }
    }
    
    //To call all releases history and sc_releases history endpoints depending on the tab selected
    function releasesHistory() {
      switch ($scope.tab) {
        case 1:
          promises.push(
            History.getReleaseHistory()
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
        sc_promises.push(
            History.getScReleasesHistory()
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
          break;
      }
    }

    //To call all permissions history and sc_permissions history endpoints depending on the tab selected
    function permissionsHistory() {
      switch ($scope.tab) {
        case 1:
          promises.push(
            History.getPermissionsHistory()
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
        sc_promises.push(
            History.getScPermissionsHistory()
              .success(function(response) {
                $scope.processResponse(response);
              })
              .error(function() {
                $scope.failed = true;
                return $q.reject();
              })
          );
          break;
      }
    }

    //To  fetch all History based on selected values and return all in one array
    function fetchHistory() {
      $scope.loading = true;
      return new Promise(function(resolve, reject) {
        if (isInArray("Rules", $scope.checkedBoxesArr)) {
          rulesHistory();
        }
        if (isInArray("Releases", $scope.checkedBoxesArr)) {
          releasesHistory();
        }
        if (isInArray("Permissions", $scope.checkedBoxesArr)) {
          permissionsHistory();
        }
        if (isInArray("Product Signoffs", $scope.checkedBoxesArr)) {
          productSignoffsHistory();
        }
        if (isInArray("Permissions Signoffs", $scope.checkedBoxesArr)) {
          permissionsSignoffsHistory();
        }
        switch($scope.tab) {
          case 1:
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
            break;
          case 2:
            $q.all(sc_promises).then(function(response) {
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
            break;
        }
      });
    }

  

    function rprscHistory() {
      $scope.optionChecked($scope.checkBoxes);
      if ($scope.checkedBoxesArr.length > 0 && $scope.checkedBoxesArr[0] !== null) {
        if ($scope.isShowUsername || $scope.isShowDaterange || $scope.isShowPrCh) {
          fetchHistory()
           .then(function(data) {
              $scope.allHistory = data;
              $scope.$apply(function() {
                if ($scope.userInput.username_email !== "") {
                  var changedByArr = [];
                  var searchResult = [];
                  $scope.userInput.username_email.forEach(function(changedBy) {
                    if (changedByArr.indexOf(changedBy.name) === -1) {
                      changedByArr.push(changedBy.name);
                      changedByArr.forEach(function(name) {
                        if (searchResult.indexOf(name) === -1) {
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
    }

    function signoffsHistory() {
      $scope.optionChecked($scope.so_checkBoxes);
      if ($scope.checkedBoxesArr.length > 0 && $scope.checkedBoxesArr[0] !== null) {
        if ($scope.isShowUsername || $scope.isShowDaterange || $scope.isShowPrCh) {
          console.log("in signoffs");
         } else {
          sweetAlert(
            "Form submission error",
            "There are no search filter fields",
            "error"
          );
        }
      }
    }

    //To search histories array based on the result gotten from fetchHistory()
    // $scope.searchHistory = function() {
    //   if ($scope.tab === 1 || $scope.tab === 2) {
    //     rprscHistory(); 
    //   } else {
    //     signoffsHistory();   
    //   }
    // };

    function checkUsernameEmail() {
      var changedByArr = [];
      $scope.userInput.username_email.forEach(function(changedBy) {
        if (changedByArr.indexOf(changedBy.name) === -1) {
          changedByArr.push(changedBy.name);
        }
      });
      return changedByArr;
    }
    

    function rprHistory () {
      $scope.search = [];
      var checkboxValues = optionChecked($scope.checkBoxes);
      if ($scope.userInput.username_email !== "") {
        var usernameValue = checkUsernameEmail();
      }
      History.getrprHistory(checkboxValues, usernameValue)
      .success(function(response) {
        angular.forEach(response, function(value, key){
          $scope.changeType = key;
          angular.forEach(value.revisions, function(revision){
            $scope.search.push(revision);
          })
        })  
      })
      .error(function() {
        console.log("error");
      })     
  }
    $scope.searchHistory = function() {
      if ($scope.tab === 1) {
        rprHistory(); 
      } else if ($scope.tab === 2) {
        soHistory();   
      } else {
        signoffHistory();
      }
    };
  });
