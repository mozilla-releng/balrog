angular.module("app").controller("NewRuleScheduledChangeCtrl",
function($scope, $http, $modalInstance, CSRF, Releases, Rules, scheduled_changes, sc, original_row, signoffRequirements, Helpers) {
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

  $scope.is_edit = false;
  $scope.scheduled_changes = scheduled_changes;
  $scope.sc = sc;
  $scope.errors = {};
  $scope.saving = false;
  $scope.calendar_is_open = false;
  $scope.sc_type = "time";

  $scope.auto_time = false;
  $scope.toggleAutoTime = function(){
      if ($scope.auto_time){
          $("#btn__auto-time").addClass('active');
      }else{
          $('#btn__auto-time').removeClass('active');
      }
  };

  $scope.$watch('sc', function() {
    if (signoffRequirements) {
      var target = $scope.sc;
      if ($scope.sc.change_type === "delete") {
        target = undefined;
      }
      $scope.scheduledChangeSignoffsRequired = Rules.ruleSignoffsRequired(original_row, target, signoffRequirements);
    }
  }, true);

  $scope.toggleType = function(newType) {
    $scope.sc_type = newType;
    $("#btn_telemetry").toggleClass("active");
    $("#btn_time").toggleClass("active");
  };

  $scope.setWhen = function(newDate) {
    if (!newDate) {
      newDate = new Date($("#id_when")[0].value);
      $scope.sc.when = newDate;
    }
    $scope.calendar_is_open = false;
    if (newDate <= new Date()) {
      $scope.errors.when = ["Scheduled time cannot be in the past"];
      $scope.sc.when = null;
    }
    else {
      $scope.errors.when = null;
    }
  };

  $scope.clearWhen = function () {
    $scope.sc.when = null;
    $scope.errors.when = null;
  };

  $scope.saveChanges = function() {
    $scope.saving = true;
    asap = new Date();
    asap.setMinutes(asap.getMinutes() + 5);
    $scope.sc.when = ($scope.auto_time) ? asap : $scope.sc.when;
    
    if ($scope.sc.change_type !== "delete") {
      // Evaluate the values entered for priority and background rate.
      $scope.integer_validation_errors = Helpers.integerValidator({'priority': $scope.sc.priority, 'backgroundRate': $scope.sc.backgroundRate});
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
    }

    CSRF.getToken()
    .then(function(csrf_token) {
      sc = angular.copy($scope.sc);
      if ($scope.sc_type === "time") {
        sc.telemetry_product = null;
        sc.telemetry_channel = null;
        sc.telemetry_uptake = null;
      }
      else {
        sc.when = null;
      }
      Rules.addScheduledChange(sc, csrf_token)
      .success(function(response) {
        $scope.sc.sc_data_version = 1;
        $scope.sc.sc_id = response.sc_id;
        $scope.sc.signoffs = response.signoffs;
        $scope.scheduled_changes.push($scope.sc);
        $modalInstance.close($scope.sc);
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
