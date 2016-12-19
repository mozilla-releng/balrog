/*global sweetAlert */
angular.module('app').controller('RuleEditCtrl',
function ($scope, $modalInstance, CSRF, Rules, Releases, rule, pr_ch_options) {

  $scope.names = [];
  Releases.getNames().then(function(names) {
    $scope.names = names;
  });
  $scope.channels = [];
  Rules.getChannels().success(function(response) {
    $scope.channels = response.channel;
  });
  $scope.products = [];
  Rules.getProducts().success(function(response) {
    $scope.products = response.product;
  });

  $scope.errors = {};
  $scope.is_edit = true;
  $scope.original_rule = rule;
  $scope.rule = angular.copy(rule);

  $scope.saving = false;
  $scope.pr_ch_options = pr_ch_options;

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRF.getToken()
    .then(function(csrf_token) {
      Rules.updateRule($scope.rule.rule_id, $scope.rule, csrf_token)
      .success(function(response) {
        $scope.rule.data_version = response.new_data_version;
        angular.copy($scope.rule, $scope.original_rule);

        if(rule.product) {
          // The first entry is special, and we want to avoid it getting sorted later.
          first_entry = $scope.pr_ch_options.shift();
          if($scope.products.indexOf(rule.product) === -1) {
            $scope.pr_ch_options.push(rule.product);
            if(rule.channel) {
              $scope.pr_ch_options.push(rule.product + "," + rule.channel);
            }
          }
          else if($scope.channels.indexOf(rule.channel) === -1) {
            $scope.pr_ch_options.push(rule.product + "," + rule.channel);
          }
          $scope.pr_ch_options.sort().unshift(first_entry);
        }

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
