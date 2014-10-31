angular.module('app').controller('NewRuleCtrl',
function($scope, $http, $modalInstance, CSRFService, Releases, Rules, rules) {

  $scope.names = [];
  Releases.getNames().then(function(names) {
    $scope.names = names;
  });

  $scope.is_edit = false;
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
    CSRFService.getToken()
    .then(function(csrf_token) {
      // set up some aliases that the data endpoint expects
      Rules.setDataAliases($scope.rule);

      rule = angular.copy($scope.rule);
      rule.backgroundRate = rule.rate;
      rule.priority = '' + rule.priority;
      Rules.addRule(rule, csrf_token)
      .success(function(response) {
        $scope.rule.data_version = 1;
        $scope.rule.rule_id = parseInt(response, 10);
        $scope.rules.push($scope.rule);
        $modalInstance.close();
      })
      .error(function(response, status) {
        if (typeof response === 'object') {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        }
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
