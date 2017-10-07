angular.module('app').controller('NewRuleCtrl',
function($scope, $http, $modalInstance, CSRF, Releases, Rules, rules, rule, pr_ch_options, signoffRequirements) {

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

  $scope.is_duplicate = !!rule._duplicate;
  $scope.is_edit = false;
  $scope.rules = rules;
  $scope.rule = rule;
  $scope.errors = {};
  $scope.saving = false;
  $scope.pr_ch_options = pr_ch_options;
  $scope.$watch('rule', function() {
    if (signoffRequirements) {
      $scope.ruleSignoffsRequired = Rules.ruleSignoffsRequired($scope.original_rule, $scope.rule, signoffRequirements);
    }
  }, true);

  $scope.saveChanges = function () {
    $scope.saving = true;
    $scope.errors = {};
    CSRF.getToken()
    .then(function(csrf_token) {
      rule = angular.copy($scope.rule);
      if(isNaN(parseInt(rule.priority, 10))|| isNaN(parseInt(rule.backgroundRate, 10))) {
        var error_source = [];
        if(isNaN(parseInt(rule.priority, 10))) {
          error_source.push('Priority');
        }
        if(isNaN(parseInt(rule.backgroundRate, 10))) {
          error_source.push('Rate');
        }
        sweetAlert(
          "Type Error",
          "Value for " + error_source.join(', ') + " should be a positive number.",
          "error"
        );
        $scope.saving = false;
        return;
      }
      if (!( 0 < rule.backgroundRate > 100)) {
        sweetAlert(
          "Value Error",
          "Value for Rate should be between 0 and 100",
          "error"
        );
        $scope.saving = false;
        return;
      }
      // rule.priority = '' + rule.priority;
      Rules.addRule(rule, csrf_token)
      .success(function(response) {
        $scope.rule.data_version = 1;
        $scope.rule.rule_id = parseInt(response, 10);
        $scope.rule.scheduled_change = null;
        $scope.rules.push($scope.rule);

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
      .error(function(response, status) {
        if (typeof response === 'object') {
          $scope.errors = response;
          console.log('ERRORS: ', $scope.errors);
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
