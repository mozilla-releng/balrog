angular.module("app").controller("DeleteRequiredSignoffsCtrl",
function ($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs,
          required_signoffs, mode, product, channel, current_user) {
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
          if (namespace[data["role"]]["sc"] === null) {
            namespace[data["role"]]["sc"] = {
              "required_signoffs": {},
              "signoffs_required": 0,
              "sc_id": response["sc_id"],
              "scheduled_by": current_user,
              "sc_data_version": 1,
              "signoffs": {},
              "change_type": "delete",
            };
          }
          // Required Signoff was previously pending, so it was directly removed
          else {
            // If it was *only* a scheduled change, we delete the whole thing
            if (namespace[data["role"]]["data_version"] === null) {
              delete namespace[data["role"]];
            }
            // If it was a scheduled change to an existing Required Signoff, just remove
            // the Scheduled Change portion
            else {
              namespace[data["role"]]["sc"] = null;
            }
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
                    "csrf_token": csrf_token};

        if ($scope.mode === "channel") {
          data["channel"] = $scope.channel;
        }
        // Not a Scheduled Change, we'll have to create one to delete it
        if ($scope.to_delete[role_name]["sc"] === null) {
          data["when"] = new Date().getTime() + 5000;
          data["change_type"] = "delete";

          service.addScheduledChange(data)
          .success(successCallback(data, deferred))
          .error(errorCallback(data, deferred));
        }
        // Already has a Scheduled Change
        else {
          var change_type = $scope.to_delete[role_name]["sc"]["change_type"];
          // If that Scheduled Change is a delete, great, nothing to do!
          if (change_type === "delete") {
            return;
          }
          // If the Scheduled Change is an insert or update, we'll need to
          // remove that. For inserts, that's all we need to do, because
          // there is no current Required Signoff to deal with.
          data["sc_data_version"] = $scope.to_delete[role_name]["sc"]["sc_data_version"];
          service.deleteScheduledChange($scope.to_delete[role_name]["sc"]["sc_id"], data)
          .success(successCallback(data, deferred))
          .error(errorCallback(data, deferred));
          // If we deleted an update, we'll need to queue up a delete to deal with
          // the current Required Signoff
          if (change_type === "update") {
            delete data["sc_data_version"];
            data["when"] = new Date().getTime() + 5000;
            data["change_type"] = "delete";

            service.addScheduledChange(data)
            .success(successCallback(data, deferred))
            .error(errorCallback(data, deferred));
          }
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
