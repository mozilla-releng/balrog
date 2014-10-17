angular.module('app').controller('RuleDeleteCtrl',
function ($scope, $modalInstance, CSRFService, RulesService, rule, rules) {

  //$scope.original_rule = rule;
  $scope.rule = rule;
  $scope.rules = rules;
  $scope.saving = false;
  // $scope.items = items;
  // $scope.selected = {
  //   item: $scope.items[0]
  // };

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRFService.getToken()
    .success(function(r, s, headers) {
      var csrf_token = headers('X-CSRF-Token');
      RulesService.deleteRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        // console.log('RESPONSE', response);
        // $scope.rule.data_version = response.new_data_version;
        // angular.copy($scope.rule, $scope.original_rule);
        $scope.rules.splice($scope.rules.indexOf($scope.rule), 1);
        $scope.saving = false;
        $modalInstance.close();
      }).error(function() {
        console.error(arguments);
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
