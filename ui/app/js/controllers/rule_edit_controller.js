/*global sweetAlert */
angular.module('app').controller('RuleEditCtrl',
function ($scope, $modalInstance, CSRFService, Rules, Releases, rule) {

  $scope.names = [];
  Releases.getNames().then(function(names) {
    $scope.names = names;
  });

  $scope.is_edit = true;
  $scope.original_rule = rule;
  $scope.rule = angular.copy(rule);

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRFService.getToken()
    .then(function(csrf_token) {
      Rules.updateRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        $scope.rule.data_version = response.new_data_version;
        angular.copy($scope.rule, $scope.original_rule);
        $scope.saving = false;
        $modalInstance.close();
      })
      .error(function(response) {
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
