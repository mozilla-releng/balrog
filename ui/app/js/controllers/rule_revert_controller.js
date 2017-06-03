angular.module('app').controller('RuleRevertCtrl',
function ($scope, $modalInstance, CSRF, Rules, revision) {

  $scope.rule = revision;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Rules.revertRule($scope.rule.rule_id, $scope.rule.change_id, csrf_token)
      .success(function(response) {
        $modalInstance.close();
      })
      .error(function() {
        console.error(arguments);
      })
      .finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
