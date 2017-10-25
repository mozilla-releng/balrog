angular.module("app").controller("HistoryDataCtrl",
function($scope, $http, $modalInstance, hs, hs_ct) {
  $scope.hs = hs;
  $scope.hs_ct = hs_ct;
  $scope.rules_modal= false;
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
