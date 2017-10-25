angular
  .module("app")
  .controller("HistoryController", function($scope, $modal, $filter, Releases, Rules, History, Page ){
    
    Page.setTitle("History");

    $scope.userInput = {
      changedBy: [],
      dateRangeStart: "",
      dateRangeEnd: "",
      hs_pr_ch_filter: ""
    };
    $scope.isShowChangedBy = true;
    $scope.isShowDaterange = true;
    $scope.isShowPrCh = true;
    $scope.allHistory = [];
    $scope.pr_ch_options = [];
    $scope.tableResult1 = false;
    $scope.tableResult2 = false;
    $scope.tableResult3 = false;
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
            $scope.pr_ch_options.sort().unshift("");
            $scope.userInput.hs_pr_ch_filter = "";
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
    $scope.productChannelValue = function(pr_ch) {
      return $scope.pr_ch_selected = pr_ch.split(",");
    };
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
          $scope.hs_pr_ch_filter = "";
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
    

    function checkParameters() {
      if ($scope.userInput.changedBy !== "") {
        var changedByArr = [];
        $scope.userInput.changedBy.forEach(function(item) {
          if (changedByArr.indexOf(item.name) === -1) {
            changedByArr.push(item.name);
          }
          $scope.changedByValue = changedByArr;
        });
      }
      if ($scope.userInput.dateRangeStart ||$scope.userInput.dateRangeEnd) { 
        $scope.hs_startDate = new Date($scope.userInput.dateRangeStart).getTime();
        $scope.hs_endDate = new Date($scope.userInput.dateRangeEnd).getTime();
      }
      if ($scope.userInput.hs_pr_ch_filter && $scope.pr_ch_selected !== undefined) {
        $scope.product = $scope.pr_ch_selected[0];
        $scope.channel = $scope.pr_ch_selected[1];   
      } else {
        return false;
      }
    }

    //Request response
    var result = [];
    function processResponse(response) {
      $scope.history_count = 0 ;
      angular.forEach(response, function(value, key){
        $scope.changeType = key;
        $scope.history_revisions = value.revisions;
        $scope.history_count += value.count;
        if ($scope.history_count > 0){
          $scope.history_revisions.forEach(function(revision){
            result.push(revision);
              $scope.search = result;
              return $scope.search;
            });
        }else {
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
      var filterParams = {
        changedByValue: $scope.changedByValue,
        startDate: $scope.hs_startDate,
        endDate: $scope.hs_endDate,
        product: $scope.product,
        channel: $scope.channel
      };
      History.getrrpHistory($scope.checkboxValues, filterParams)
      .success(function(response) {
        if(Object.keys(response).length > 0){
          $scope.tableResult1 = true;
          processResponse(response); 
        } else {
          $scope.search = [];
          $scope.tableResult1 = false;
          return $scope.search;
        }   
      })
      .error(function() {
        console.log("error");
      });
    }

    function scHistory() {
      checkParameters();
      var filterParams = {
        changedByValue: $scope.changedByValue,
        startDate: $scope.hs_startDate,
        endDate: $scope.hs_endDate,
        product: $scope.product,
        channel: $scope.channel
      };
      History.getscHistory($scope.checkboxValues, filterParams)
      .success(function(response) {
        if(Object.keys(response).length > 0){
          $scope.tableResult2 = true;
          processResponse(response); 
        } else {
          $scope.search = [];
          $scope.tableResult2 = false;
          return $scope.search;
        }   
      })
      .error(function() {
        console.log("error");
      });   
    }

    function signoffHistory() {
      checkParameters();
      var filterParams = {
        changedByValue: $scope.changedByValue,
        startDate: $scope.hs_startDate,
        endDate: $scope.hs_endDate,
        product: $scope.product,
        channel: $scope.channel
      };
      History.getsignoffHistory($scope.checkboxValues, filterParams)
      .success(function(response) {
        if(Object.keys(response).length > 0){
          $scope.tableResult3 = true;
          processResponse(response); 
        } else {
          $scope.search = [];
          $scope.tableResult3 = false;
          return $scope.search;
        }   
      })
      .error(function() {
        console.log("error");
      });   
    }

    function optionChecked(choice) {
      angular.forEach(choice, function(value, key) {
        if (choice[key].selected) {
          $scope.constants[choice[key].name] = 1;
        }else{
          $scope.constants[choice[key].name] = 0;
        }
      });
      return $scope.constants;
    }

    $scope.searchHistory = function() {
      
      switch ($scope.tab) {
        case 1:
          var rrp_constants = {rules: 0, releases:0, permissions:0 };
          $scope.constants = rrp_constants;
          $scope.checkboxValues = optionChecked($scope.checkBoxes);
          rrpHistory(); 
          break;
        case 2:
          var sc_constants = {
            rules_scheduled_change: 0,
            releases_scheduled_change:0,
            permissions_scheduled_change:0,
            permissions_required_signoff_scheduled_change:0,
            product_required_signoff_scheduled_change:0
          };
          $scope.constants = sc_constants;
          $scope.checkboxValues = optionChecked($scope.sc_checkBoxes);
          scHistory(); 
          break;
        case 3:
          var signoff_constants = {
            permissions_required_signoffs: 0,
            product_required_signoffs:0
          };
          $scope.constants = signoff_constants;
          $scope.checkboxValues = optionChecked($scope.signoff_checkBoxes);
          signoffHistory();
          break;
      }
    };

    $scope.openDataModal = function(change_id) {
      angular.forEach($scope.search, function(revision){
        if(revision.change_id === change_id ){
          var modalInstance = $modal.open({
            templateUrl: 'history_data_modal.html',
            controller: 'HistoryDataCtrl',
            size: 'lg',
            backdrop: 'static',
            resolve: {
              hs: function() {
                var hs = revision;
                return hs;
              },
              hs_ct: function() {
                var hs_ct = $scope.changeType;
                return hs_ct;
              },
            }
          });
        } 
      });
          
    };
    
  
  });
