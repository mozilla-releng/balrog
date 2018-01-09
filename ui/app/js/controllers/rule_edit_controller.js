/*global sweetAlert */
angular.module('app').controller('RuleEditCtrl',
function ($scope, $modalInstance, CSRF, Rules, Releases, rule, signoffRequirements, pr_ch_options, Helpers) {

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
  $scope.signoffRequirements = signoffRequirements;
  $scope.$watch('rule', function() {
    if (signoffRequirements) {
      $scope.ruleSignoffsRequired = Rules.ruleSignoffsRequired($scope.original_rule, $scope.rule, $scope.signoffRequirements);
    }
  }, true);


  $scope.saving = false;
  $scope.pr_ch_options = pr_ch_options;

  $scope.saveChanges = function () {
   var r = confirm("You have changed the channel value. This can have unexpected impacts\n\nClick 'OK' to Confirm The Changes");
   if (r == true) {
    $scope.saving = true;

    // Evaluate the values entered for priority and background rate.
    $scope.integer_validation_errors = Helpers.integerValidator({'priority': $scope.rule.priority, 'backgroundRate': $scope.rule.backgroundRate});
    // Stop sending the request if any number validation errors.
    if($scope.integer_validation_errors.priority || $scope.integer_validation_errors.backgroundRate) {
      $scope.saving = false;
      sweetAlert(
        "Form submission error",
        "See fields highlighted in red.",
        "error"
      );
      return;
    }

    CSRF.getToken()
    .then(function(csrf_token) {
      // The data we need to submit is a tweaked version of just the Rule fields, so
      // we need to remove the scheduled change object before submission.
      var data = angular.copy($scope.rule);
      if (data.scheduled_change) {
        delete data.scheduled_change;
      }
      Rules.updateRule($scope.rule.rule_id, data, csrf_token)
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
   }
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

