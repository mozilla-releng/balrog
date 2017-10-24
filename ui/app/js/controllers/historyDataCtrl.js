angular.module("app").controller("HistoryDataCtrl",
function($scope, $http, $modalInstance, hs) {
    $scope.hs = hs;
    console.log($scope.hs,"gettng in modal controller");
  
 
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
