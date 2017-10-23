angular
  .module("app")
  .controller("HistoryController", function($scope, $q, $modal, $filter, Releases, Rules, History, Page ){
    
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
    $scope.tableResult = false;
    $scope.calendar_is_open = false;
    $scope.loading = false;
    $scope.failed = false;
    $scope.tab = 1;
    $scope.rrpfilter = true;
    $scope.search = [];
    

    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.maxSize = 10;

    // Setting tabs
    $scope.setTab = function(newTab) {
      $scope.tab = newTab;
      if ($scope.tab === 1 || $scope.tab === 2) {
        $scope.rrpfilter = true;
        $scope.so_filter = false;
      } else if ($scope.tab === 3){
        $scope.rrpfilter = false;
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
          $scope.msg = "Filtering will be done in: " +$scope.checkedBoxesArr[choice[key].name];  
        }
        else{
          $scope.checkedBoxesArr[choice[key].name] = 0;
          // sweetAlert("Form submission error", "Please check a box", "error");
        }   
      });
      return $scope.checkedBoxesArr;
    }

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
      $scope.userInput.username_email = "";
    };
    $scope.hideDaterange = function() {
      $scope.isShowDaterange = false;
      $scope.userInput.dateRangeStart = "";
      $scope.userInput.dateRangeEnd = "";
    };
    $scope.hidePrCh = function() {
      $scope.isShowPrCh = false;
    };
    //End add and remove filter fields
    
    
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

    function checkUsernameEmail() {
      var changedByArr = [];
      $scope.userInput.username_email.forEach(function(changedBy) {
        if (changedByArr.indexOf(changedBy.name) === -1) {
          changedByArr.push(changedBy.name);
        }
      });
      return changedByArr;
    }


    function checkParameters() {
      $scope.checkboxValues = optionChecked($scope.checkBoxes);
      if ($scope.userInput.username_email !== "") {
        $scope.usernameValue = checkUsernameEmail();
      }
    }


    var result = [];
    function processResponse(response) {
      $scope.tableResult = true;
      angular.forEach(response, function(value, key){
        // console.log(response,"response");
        $scope.changeType = key;
        $scope.rrp_count = value.count;
        $scope.rrp_revisions = value.revisions;
        if($scope.rrp_count !== 0){
          $scope.rrp_revisions.forEach(function(revision){
            result.push(revision);
            $scope.search = result;
          });
        }
        else{
          sweetAlert(
            "error",
            "No results matching the filter",
            "error"   
          );
        }
      }); 
    }

    
    
    function rrpHistory () {    
      checkParameters();
      History.getrrpHistory($scope.checkboxValues, $scope.usernameValue)
      .success(function(response) {
        processResponse(response);  
      })
      .error(function() {
        console.log("error");
      });
    }

    function scHistory() {
      checkParameters();
      History.getscHistory($scope.checkboxValues, $scope.usernameValue)
      .success(function(response) {
        processResponse(response);  
      })
      .error(function() {
        console.log("error");
      });   
    }

    function signoffHistory() {
      checkParameters();
      History.getscHistory($scope.checkboxValues, $scope.usernameValue)
      .success(function(response) {
        processResponse(response);  
      })
      .error(function() {
        console.log("error");
      });   
    }

    $scope.searchHistory = function() {
      switch ($scope.tab) {
        case 1:
          rrpHistory(); 
          break;
        case 2:
          scHistory(); 
          break;
        case 3:
          signoffHistory();
          break;
      }
    };

    function isInArray(id, result) {
      for (var i = 0; i < result.length; i++) {
        if (result[i] === id) {
          return true;
        }
      }
      return false;
    }

    $scope.openDataModal = function(change_id) {
      angular.forEach($scope.search, function(revision){
        if(revision.change_id === change_id ){
          console.log(revision.change_id,"found");
          var modalInstance = $modal.open({
            templateUrl: 'history_data_modal.html',
            controller: 'HistoryDataCtrl',
            size: 'lg',
            backdrop: 'static',
            resolve: {
              hs: function() {
                var hs = angular.copy($scope.search);
                hs.original_row = hs;
                return hs;
              },
            }
          });
        } 
      });
          
    };
    
  
  });
