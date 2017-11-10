angular.module('app').controller('ScheduledReleaseUpdateDataCtrl',
function($scope, $http, $modalInstance, Releases, Rules, sc, diff) {
$scope.sc= sc;
$scope.diff = diff;

if (sc.sc_id){
    if(diff){
        Releases.getUpDiff(sc.sc_id)
        .then(function(response){
            $scope.sc.diff = response.data;
        });
    }
}
$scope.cancel = function () {
$modalInstance.dismiss('cancel');
};
});

