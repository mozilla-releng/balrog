angular
  .module("app")
  .controller("HistoryController", function($scope, $modal, $filter, Releases, Rules, History, Page ){
    
    Page.setTitle("History");

    $scope.userInput = {
      changedBy: "",
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
    $scope.pageSize = 10;
    $scope.maxSize = 5;

    $scope.data = {
      objectOptions: [
        {id: '1', name: 'default', value:'---Please select---' },
        {id: '2', name: 'rules', value: 'Rules'},
        {id: '3', name: 'releases', value: 'Releases'},
        {id: '4', name: 'permissions', value: 'Permissions'},
        {id: '5', name: 'product_required_signoffs', value: 'Product Required Signoffs'},
        {id: '6', name: 'permissions_required_signoffs', value: 'Permissions Required Signoffs'},
      ],
      objectSelected:{id: '1',  name: 'default', value:'---Please select---' }
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
   
    function checkParameters() {
      if ($scope.data.objectSelected.id !== '1') {
        $scope.objectValue = $scope.data.objectSelected.name;
      }else{
        sweetAlert(
          "Please select an object",
          "You cannot proceed",
          "error"
        );
      }
      if ($scope.userInput.changedBy !== ""){
        $scope.changedByValue = $scope.userInput.changedBy.toLowerCase();
      }
      else {
        $scope.changedByValue = "";
      }
      if ($scope.userInput.dateRangeStart && $scope.userInput.dateRangeEnd) { 
        $scope.hs_startDate = new Date($scope.userInput.dateRangeStart).getTime();
        $scope.hs_endDate = new Date($scope.userInput.dateRangeEnd).getTime();
      }
      else {
        $scope.hs_startDate = "";
        $scope.hs_endDate = "";
      }
      if ($scope.userInput.hs_pr_ch_filter && $scope.pr_ch_selected !== undefined) {
        $scope.product = $scope.pr_ch_selected[0];
        $scope.channel = $scope.pr_ch_selected[1];   
      } 
      else {
        $scope.product = "";
        $scope.channel = "";
      }
    }


    $scope.searchHistory = function() {
      $scope.searchResult = [];
      $scope.loading = true;
      checkParameters();
      var filterParams = {
        objectValue: $scope.objectValue,
        changedByValue: $scope.changedByValue,
        startDate: $scope.hs_startDate,
        endDate: $scope.hs_endDate,
        product: $scope.product,
        channel: $scope.channel
      };
      History.getHistory(filterParams)
      .success(function(response) {
        $scope.tableResult = true;
        var result = [];
        $scope.changeType = [];
        $scope.history_count = 0;
        angular.forEach(response, function(value, key){
          $scope.history_revisions = value.revisions;
          $scope.history_required_signoffs = value.required_signoffs;
          $scope.history_count += value.count;
          if ($scope.history_count > 0){
            if($scope.history_required_signoffs){
              $scope.history_required_signoffs.forEach(function(revision){
                $scope.revision = revision;
                $scope.revision["type"] = key;
                result.push($scope.revision);
              });
            }
            if($scope.history_revisions){  
              $scope.history_revisions.forEach(function(revision){
                $scope.revision = revision;
                $scope.revision["type"] = key;
                result.push($scope.revision);                
              });
          }
          $scope.searchResult = result;
        }
          else {
              sweetAlert(
                "error",
                "No results matching the filter",
                "error"   
              );
            }      });         
      })
      .error(function() {
        console.error(arguments);
        $scope.failed = true;
      })
      .finally(function() {
        $scope.loading = false;
      });
    };

    $scope.orderHistory = function(revision) {
      if (revision.timestamp) {
          return revision.timestamp * -1;
      }
    };

    $scope.clearFilters = function() {
      $scope.data.objectSelected = {id: '1',  name: 'default', value:'---Please select---' },
      $scope.userInput = {
        changedBy: "",
        dateRangeStart: "",
        dateRangeEnd: "",
        hs_pr_ch_filter: ""
      };
    }

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
            }
          });
        } 
      });       
    };
  });
