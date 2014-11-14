angular.module('app').controller('RuleRevertCtrl',
function ($scope, $modalInstance, CSRF, Rules, revision) {

  $scope.rule = revision;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Rules.revertRule($scope.rule.id, $scope.rule.change_id, csrf_token)
      .success(function(response) {
        $scope.saving = false;
        $modalInstance.close();
      })
      .error(function() {
        $scope.saving = false;
        console.error(arguments);
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
