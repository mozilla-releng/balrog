angular.module('app').controller('RuleDeleteCtrl',
function ($scope, $modalInstance, CSRFService, Rules, rule, rules) {

  $scope.rule = rule;
  $scope.rules = rules;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRFService.getToken()
    .then(function(csrf_token) {
      Rules.deleteRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        $scope.rules.splice($scope.rules.indexOf($scope.rule), 1);
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
