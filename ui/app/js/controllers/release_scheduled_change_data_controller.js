angular.module('app').controller('ReleaseScheduledChangeDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, release, diff) {
  $scope.release = release;
  $scope.diff = diff;

   

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
