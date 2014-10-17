angular.module('app').controller('RuleEditCtrl',
function ($scope, $modalInstance, CSRFService, RulesService, ReleasesService, rule) {

  $scope.names = [];
  ReleasesService.getNames().then(function(names) {
    $scope.names = names;
  });

  $scope.original_rule = rule;
  $scope.rule = angular.copy(rule);

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRFService.getToken()
    .then(function(csrf_token) {
      RulesService.updateRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        // console.log('RESPONSE', response);
        $scope.rule.data_version = response.new_data_version;
        angular.copy($scope.rule, $scope.original_rule);
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
