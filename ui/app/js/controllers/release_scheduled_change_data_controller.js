angular.module('app').controller('ReleaseScheduledChangeDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, release, diff) {
  $scope.release = release;
  $scope.diff = diff;

  
  if(release.change_type==="delete"){
  	Releases.getRelease(release.name)
      .then(function(response) {
        $scope.release.data = response.data;
      });
  } 
  
  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});