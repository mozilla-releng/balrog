angular.module('app').controller('RuleRevertCtrl',
function ($scope, $modalInstance, CSRFService, RulesService, rule) {

  $scope.rule = rule;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRFService.getToken()
    .then(function(csrf_token) {
      RulesService.revertRule($scope.rule.id, $scope.rule.change_id, csrf_token)
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
