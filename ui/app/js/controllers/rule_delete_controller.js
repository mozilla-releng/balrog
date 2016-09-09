angular.module('app').controller('RuleDeleteCtrl',
function ($scope, $modalInstance, CSRF, Rules, rule, rules) {

  $scope.rule = rule;
  $scope.rules = rules;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Rules.deleteRule($scope.rule.rule_id, $scope.rule, csrf_token)
      .success(function(response) {
        $scope.rules.splice($scope.rules.indexOf($scope.rule), 1);
        $modalInstance.close();
      })
      .error(function(response) {
        if (typeof response === 'object') {
          sweetAlert(response.exception);
        }
        console.error(response);
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
