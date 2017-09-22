angular.module("app").controller('HistoryController',
function($scope, Releases, Page) {
    Page.setTitle('History');
    
    $scope.tab = 1;
    $scope.rowtab = "#rulesHistory";
    $scope.filter = [];
    $scope.username = "";
    $scope.timestamp = "";
    $scope.product_channel = "";

    $scope.setTab = function(newTab){
        $scope.tab = newTab;
    };

    $scope.isSet = function(tabNum){
        return $scope.tab === tabNum;
    };

    $scope.tabChange = function(e){
        if (e.target.nodeName === 'A') {
            $scope.rowtab = e.target.getAttribute("href");
            e.preventDefault();
        }
    }

    $scope.$watch('filtering_str', function(value) {
        $scope.filtering = value.value.split(',');
      });
    $scope.filtering_options = [
        {
        text: "All",
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
        },
    ];
    $scope.filtering_str = $scope.filtering_options[0];

    $scope.filterSelected = function(value) {
        $scope.filter.push(value);
    }

    $scope.history = [];
    $scope.isShowUsername = true;
    $scope.isShowTimestamp = true;
    $scope.isShowPrCh = true;
    $scope.hideUsername = function () {
        $scope.isShowUsername = $scope.isShowUsername ? false : true;
    }
    $scope.hideTimestamp = function () {
        $scope.isShowTimestamp = $scope.isShowTimestamp ? false : true;
    }
    $scope.hidePrCh = function () {
        $scope.isShowPrCh = $scope.isShowPrCh ? false : true;
    }

   
    

    // Releases.getReleases().success(function(response) {
    //     console.log(response.releases,"respon");
    //     // $scope.release_response = response.releases;
    //     // Releases.getHistory($scope.release_response)
    //     // .success(function(response) {
    //     // });
    // });

    




});
