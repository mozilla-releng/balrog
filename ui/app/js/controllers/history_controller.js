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
    $scope.allHistory = [];
    $scope.pr_ch_options = [];
    $scope.tableResult = false;
    $scope.calendar_is_open = false;
    $scope.loading = false;
    $scope.failed = false;
    $scope.searchResult = [];
    $scope.checkBoxes = {};
    
    $scope.currentPage = 1;
    $scope.pageSize = 100;
    $scope.maxSize = 10;

    $scope.checkbox_constants  = {
      rules: 0,
      releases:0,
      permissions: 0,
      permissions_required_signoffs: 0,
      product_required_signoffs:0
    };
      
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

    
    function optionChecked(choice) {
      angular.forEach(choice, function(value, key) {
        if (value === true) {
          $scope.checkbox_constants[key]= 1; 
        }else{
          $scope.checkbox_constants[key] = 0;
        }
      });
      return $scope.checkbox_constants;
    }
    
    function checkParameters() {
      $scope.checkboxValues = optionChecked($scope.checkBoxes);
      angular.forEach($scope.checkboxValues, function(value, key){
        if (value === 1) {
          if ($scope.userInput.changedBy) {
            var changedByArr = [];
            $scope.userInput.changedBy.forEach(function(item) {
              if (changedByArr.indexOf(item.name) === -1) {
                changedByArr.push(item.name);
              }
              $scope.changedByValue = changedByArr;
            });
          }
          if ($scope.userInput.dateRangeStart && $scope.userInput.dateRangeEnd) { 
            $scope.hs_startDate = new Date($scope.userInput.dateRangeStart).getTime();
            $scope.hs_endDate = new Date($scope.userInput.dateRangeEnd).getTime();
          }
          if ($scope.userInput.hs_pr_ch_filter && $scope.pr_ch_selected !== undefined) {
            $scope.product = $scope.pr_ch_selected[0];
            $scope.channel = $scope.pr_ch_selected[1];   
          } 
        } else {
          // sweetAlert(
          //   "Please check a box",
          //   "You cannot proceed",
          //   "error"
          // );
        }
      })
    }

    //Request response
    function processResponse(response) {
      var result = [];
      $scope.history_count = 0;
      angular.forEach(response, function(value, key){
        $scope.changeType = key;
        $scope.history_revisions = value.revisions;
        $scope.history_count += value.count;
        if ($scope.history_count > 0){
          $scope.history_revisions.forEach(function(revision){
            result.push(revision);
          });
        }else {
            sweetAlert(
              "error",
              "No results matching the filter",
              "error"   
            );
          }
      });         
      $scope.searchResult = result;
      
    }
    //Request response ends


    $scope.searchHistory = function() {
      $scope.loading = true;
      checkParameters();
      var filterParams = {
        checkboxValue: $scope.checkboxValues,
        changedByValue: $scope.changedByValue,
        startDate: $scope.hs_startDate,
        endDate: $scope.hs_endDate,
        product: $scope.product,
        channel: $scope.channel
      };
      History.getHistory(filterParams)
      .success(function(response) {
        if(Object.keys(response).length > 0){
          $scope.tableResult = true;
          processResponse(response); 
        } else {
          $scope.searchResult = [];
          $scope.tableResult = false;
          return $scope.searchResult;
        }
      })
      .error(function() {
        console.error(arguments);
        $scope.failed = true;
      })
      .finally(function() {
        $scope.loading = false;
      });
    };

    $scope.openDataModal = function(change_id) {
      angular.forEach($scope.searchResult, function(revision){
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
