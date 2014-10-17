angular.module('app').controller('NewRuleCtrl',
function($scope, $http, $modalInstance, CSRFService, ReleasesService, RulesService, rules) {

  $scope.names = [];
  ReleasesService.getNames().then(function(names) {
    $scope.names = names;
  });

  $scope.rules = rules;
  $scope.rule = {
    product: '',
    rate: 0,
    priority: 0,
    update_type: 'minor',
  };
  $scope.errors = {};
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;
    $scope.errors = {};
    // console.log('NEW RULE', $scope.rule);
    CSRFService.getToken()
    .then(function(csrf_token) {
      // need to change to names the server expects
      rule = angular.copy($scope.rule);
      rule.backgroundRate = rule.rate;
      rule.priority = '' + rule.priority;
      RulesService.addRule(rule, csrf_token)
      .success(function(response) {
        $scope.rule.data_version = 1;
        $scope.rule.id = parseInt(response, 10);
        $scope.rules.push($scope.rule);
        $modalInstance.close();
      }).error(function(response) {
        if (typeof response === 'object') {
          $scope.errors = response;
        }
      }).finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
