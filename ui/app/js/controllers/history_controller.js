angular
  .module("app")
  .controller("HistoryController", function($scope, $q, $modal, $filter, Releases, Rules, History, Page ){
    
    Page.setTitle("History");

    $scope.userInput = {
      changedBy: [],
      dateRangeStart: "",
      dateRangeEnd: "",
      hs_pr_ch_filter: "All Rules"
    };
    $scope.isShowChangedBy = true;
    $scope.isShowDaterange = true;
    $scope.isShowPrCh = true;
    $scope.allHistory = [];
    $scope.pr_ch_options = [];
    $scope.tableResult = false;
    $scope.calendar_is_open = false;
    $scope.loading = false;
    $scope.failed = false;
    $scope.tab = 1;
    $scope.rrp_filter = true;
    $scope.search = [];
    

    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.maxSize = 10;

    // Setting tabs
    $scope.setTab = function(newTab) {
      $scope.tab = newTab;
      if ($scope.tab === 1) {
        $scope.rrp_filter = true;
        $scope.sc_filter = false;
        $scope.signoff_filter = false;
      } else if ($scope.tab === 2){
        $scope.sc_filter = true;
        $scope.signoff = false;
        $scope.rrp_filter = false;
      } else {
        $scope.signoff_filter = true;
        $scope.rrp_filter = false;
        $scope.sc_filter = false;
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

    $scope.sc_checkBoxes = [
      {
        id: 1,
        name: "rules_scheduled_change",
        value: "Rules",
        selected: false
      },
      {
        id: 2,
        name: "releases_scheduled_change",
        value: "Releases",
        selected: false
      },
      {
        id: 3,
        name: "permissions_scheduled_change",
        value: "Permissions",
        selected: false
      },
      {
        id: 4,
        name: "product_required_signoff_scheduled_change",
        value: "Product Signoffs",
        selected: false
      },
      {
        id: 5,
        name: "permissions_required_signoff_scheduled_change",
        value: "Permissions Signoffs",
        selected: false
      }
    ];


    $scope.signoff_checkBoxes = [
      {
        id: 1,
        name: "product_required_signoffs",
        value: "Product Signoffs",
        selected: false
      },
      {
        id: 2,
        name: "permissions_required_signoffs",
        value: "Permissions Signoffs",
        selected: false
      }
    ];

    function optionChecked(choice) {
      switch($scope.tab){
        case 1:
          var rrp_constants = {rules: 0, releases:0, permissions:0 };
          angular.forEach(choice, function(value, key) {
            (choice[key].selected) ?
            rrp_constants[choice[key].name] = 1 :
            rrp_constants[choice[key].name] = 0
          });
          return rrp_constants;
          break;
        case 2:
          var sc_constants = {
            rules_scheduled_change: 0,
            releases_scheduled_change:0,
            permissions_scheduled_change:0,
            permissions_required_signoff_scheduled_change:0,
            product_required_signoff_scheduled_change:0
          };
          angular.forEach(choice, function(value, key) {
            (choice[key].selected) ?
            sc_constants[choice[key].name] = 1 :
            sc_constants[choice[key].name] = 0
          });
          return sc_constants;
          break;
        case 3:
          var signoff_constants = {
            permissions_required_signoffs: 0,
            product_required_signoffs:0
          };
          angular.forEach(choice, function(value, key) {
            (choice[key].selected) ?
            signoff_constants[choice[key].name] = 1 :
            signoff_constants[choice[key].name] = 0 
          });
          return signoff_constants;
          break;
      }
    }
      

    //Add and remove username or email tags
    $scope.addChangedBy = function() {
      $scope.userInput.changedBy.push({ name: $scope.changedBy });
      $scope.changedBy = "";
    };

    $scope.deleteChangedBy= function(key) {
      if ($scope.userInput.changedBy.length > 0 && $scope.changedBy.length === 0 &&
        key === undefined) {
        $scope.userInput.changedBy.pop();
      } else if (key !== undefined) {
        $scope.userInput.changedBy.splice(key, 1);
      }
    };
    // User/email tag ends

    //Check for repeated names 
    function checkChangedBy() {
      var changedByArr = [];
      $scope.userInput.changedBy.forEach(function(item) {
        if (changedByArr.indexOf(item.name) === -1) {
          changedByArr.push(item.name);
        }
      });
      return changedByArr;
    }

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
        case "changedBy":
          $scope.isShowChangedBy = true;
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

    $scope.hideChangedBy = function() {
      $scope.isShowChangedBy = false;
      $scope.userInput.changedBy = "";
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
    
    
    // function signoffsHistory() {
    //   $scope.optionChecked($scope.so_checkBoxes);
    //   if ($scope.rrpConstants.length > 0 && $scope.rrpConstants[0] !== null) {
    //     if ($scope.isShowUsername || $scope.isShowDaterange || $scope.isShowPrCh) {
    //       console.log("in signoffs");
    //      } else {
    //       sweetAlert(
    //         "Form submission error",
    //         "There are no search filter fields",
    //         "error"
    //       );
    //     }
    //   }
    // }

    


    function checkParameters() {
      switch($scope.tab){
        case 1:
          $scope.checkboxValues = optionChecked($scope.checkBoxes);
          break;
        case 2:
          $scope.checkboxValues = optionChecked($scope.sc_checkBoxes);
          break;
        case 3:
          $scope.checkboxValues = optionChecked($scope.signoff_checkBoxes);
          break;
      }
      if ($scope.userInput.changedBy !== "") {
        $scope.changedByValue = checkChangedBy();
      }
    }

    //Request response
    var result = [];
    function processResponse(response) {
      console.log(response,"response");
      $scope.tableResult = true;
      angular.forEach(response, function(value, key){
        $scope.changeType = key;
        $scope.history_count = value.count;
        $scope.history_revisions = value.revisions;
        if($scope.history_count !== 0){
          $scope.history_revisions.forEach(function(revision){
            result.push(revision);
            $scope.search = result;
          });
          console.log($scope.search,"result");
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
    //Request response ends

    
    
    function rrpHistory () {    
      checkParameters();
      History.getrrpHistory($scope.checkboxValues, $scope.changedByValue)
      .success(function(response) {
        processResponse(response);  
      })
      .error(function() {
        console.log("error");
      });
    }

    function scHistory() {
      checkParameters();
      History.getscHistory($scope.checkboxValues, $scope.changedByValue)
      .success(function(response) {
        processResponse(response);  
      })
      .error(function() {
        console.log("error");
      });   
    }

    function signoffHistory() {
      checkParameters();
      History.getsignoffHistory($scope.checkboxValues, $scope.changedByValue)
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
