angular.module("app").controller("DeleteRequiredSignoffsCtrl",
function ($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
          required_signoffs, mode, product, channel) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.required_signoffs = required_signoffs;
  $scope.mode = mode;
  $scope.product = product;
  $scope.channel = channel;
  $scope.to_delete = {};
  $scope.title = "Remove Signoff Requirements for ";

  if ($scope.mode === "channel") {
    $scope.to_delete = $scope.required_signoffs[$scope.product]["channels"][$scope.channel];
    $scope.title += " for the " + $scope.product + " " + $scope.channel + " channel";
  }
  else {
    $scope.to_delete = $scope.required_signoffs[$scope.product]["permissions"];
    $scope.title += " for " + $scope.product + " Permissions";
  }

  $scope.saveChanges = function() {
    $scope.errors = {};

    var service = null;
    if ($scope.mode === "channel") {
      service = ProductRequiredSignoffs;
    }
    else if ($scope.mode === "permissions") {
      service = PermissionsRequiredSignoffs;
    }
    else {
      $scope.errors["exception"] = "Couldn't detect mode";
      return;
    }

    console.log(required_signoffs);
    console.log($scope.to_delete);

    CSRF.getToken()
    .then(function(csrf_token) {
      $scope.saving = true;
      var promises = [];

      var successCallback = function(data, deferred) {
        return function(response) {
          var namespace = null;
          if ($scope.mode === "channel") {
            namespace = required_signoffs[$scope.product]["channels"][$scope.channel];
          }
          else {
            namespace = required_signoffs[$scope.product]["permissions"];
          }

          // Required Signoff wasn't pending, so a deletion will be a new Scheduled Change
          if (namespace[data["role"]]["sc_id"] === null) {
            namespace[data["role"]]["sc_id"] = response["sc_id"];
            namespace[data["role"]]["sc_data_version"] = 1;
            namespace[data["role"]]["change_type"] = "delete";
          }
          // Required Signoff was previously pending, so it was directly removed
          else {
            delete namespace[data["role"]];
          }

          deferred.resolve();
        };
      };
      var errorCallback = function(data, deferred) {
        return function(response, status) {
          if (typeof response === "object") {
            $scope.errors = response;
          }
          else if (typeof response === "string"){
            $scope.errors["exception"] = response;
          }
          else {
            sweetAlert("Unknown error occurred");
          }
          deferred.resolve();
        };
      };

      Object.keys($scope.to_delete).forEach(function(role_name) {
        var deferred = $q.defer();
        promises.push(deferred.promise);
        var data = {"product": $scope.product, "role": role_name, "data_version": $scope.to_delete[role_name]["data_version"],
                    "csrf_token": csrf_token, "sc_data_version": $scope.to_delete[role_name]["sc_data_version"]};
                    
        if ($scope.mode === "channel") {
          data["channel"] = $scope.channel;
        }
        if ($scope.to_delete[role_name]["sc_id"] === null) {
          data["when"] = new Date().getTime() + 5000;
          data["change_type"] = "delete";

          service.addScheduledChange(data)
          .success(successCallback(data, deferred))
          .error(errorCallback(data, deferred));
        }
        else {
          service.deleteScheduledChange($scope.to_delete[role_name]["sc_id"], data)
          .success(successCallback(data, deferred))
          .error(errorCallback(data, deferred));
        }
      });

      $q.all(promises)
      .then(function() {
        if (Object.keys($scope.errors).length === 0) {
          $modalInstance.close();
        }
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss("cancel");
  };
});
