angular.module("app").controller('HistoryController',
function($scope, Page) {
    Page.setTitle('History');
    
    $scope.filter = [
        {username: ""},
        {timestamp: ""},
        {product_channel: ""}
    ];
    // $scope.username = "";
    // $scope.timestamp = "";
    // $scope.product_channel = "";

    $scope.$watch('filtering_str', function(value) {
        $scope.filtering = value.value.split(',');
      });
    $scope.filtering_options = [
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



});
