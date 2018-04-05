angular.module("app").controller("HistoryDataCtrl",
function($scope, $http, $modalInstance, hs) {
  $scope.hs = hs;
  $scope.rules_modal= false;
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
