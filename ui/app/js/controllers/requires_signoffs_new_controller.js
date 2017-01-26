angular.module("app").controller("NewRequiredSignoffCtrl",
function($scope, $modalInstance, $q, CSRF, ProductRequiredSignoffs, PermissionsRequiredSignoffs, required_signoffs) {
  $scope.saving = false;
  $scope.errors = {};

  $scope.mode = "channel";
  $scope.product = "";
  $scope.channel = "";
  $scope.new_roles = 1;

  $scope.getTitle = function () {
    var title = "Signoff Requirements";
    if ($scope.product !== "") {
      if ($scope.mode === "channel" && $scope.channel !== "") {
        title += " for the " + $scope.product + " " + $scope.channel + " channel";
      }
      else if ($scope.mode === "permissions") {
        title += " for " + $scope.product + " Permissions";
      }
    }
    return title;
  };

  $scope.saveChanges = function() {
    $scope.errors = {};

    var new_required_signoffs = {};

    // Collect all of the new roles and signoff requirements
    $("#new_roles > .new_role").each(function(index, rs) {
      console.log(rs);
      rs = $(rs);
      var role = rs.find("input[name='role']")[0].value;
      var signoffs_required = rs.find("input[name='signoffs_required']")[0].value;
      if (role !== "") {
        if (role in new_required_signoffs) {
          $scope.errors["role"] = "Cannot specify any Role more than once.";
        }
        else {
          new_required_signoffs[role] = signoffs_required;
        }
      }
    });

    if (Object.keys(new_required_signoffs).length === 0) {
      $scope.errors["exception"] = "No new roles found!";
    }

    if (Object.keys($scope.errors).length === 0) {
      $scope.saving = true;

      CSRF.getToken()
      .then(function(csrf_token) {
        var service = null;
        var first = true;

        var promises = [];

        if ($scope.mode === "channel") {
          service = ProductRequiredSignoffs;
        }
        else if ($scope.mode === "permissions") {
          service = PermissionsRequiredSignoffs;
        }
        else {
          $scope.errors["exception"] = "Couldn't detect mode";
          $scope.saving = false;
        }

        var successCallback = function(data) {
          return function(response) {
            var data_version = response["new_data_version"];
            // todo: maybe required_signoffs should be an object with methods
            // so we don't have to duplicate this from the main controller
            if (! (data["product"] in required_signoffs)) {
              required_signoffs[data["product"]] = {"channels": {}};
            }

            // TODO: this isn't updating the page properly. also need to close the modal
            if ($scope.mode === "channel") {
              if (! (data["channel"] in required_signoffs[data["product"]]["channels"])) {
                required_signoffs[data["product"]]["channels"][data["channel"]] = {};
              }
              required_signoffs[data["product"]]["channels"][data["channel"]][data["role"]] = {
                "signoffs_required": data["signoffs_required"],
                "data_version": data_version,
              };
            }
            else if ($scope.mode === "permissions") {
            }
          };
        };
        var errorCallback = function(data) {
          return function(response, status) {
            console.log("got error");
            console.log(response);
            if (typeof response === "object") {
              $scope.errors = response;
            }
            else if (typeof response === "string"){
              $scope.errors["exception"] = response;
            }
            else {
              sweetAlert("Unknown error occurred");
            }
            console.log($scope.errors);
          };
        };

        for (var role in new_required_signoffs) {
          var d = $q.defer();
          var data = {"product": $scope.product, "role": role, "signoffs_required": new_required_signoffs[role], "csrf_token": csrf_token};
          if ($scope.mode === "channel") {
            data["channel"] = $scope.channel;
          }
          if (first) {
            service.addRequiredSignoff(data)
            .success(successCallback(data))
            .error(errorCallback(data))
            .finally(function() { d.resolve(); });
            promises.push(d.promise);
          }
          else {
            // todo: add rs stuff to data
            service.addScheduledChange(data)
            .success(successCallback(data))
            .error(errorCallback(data));
          }
        }

$q.all(promises)
.then(function() {
    console.log("firing");
    if (Object.keys($scope.errors).length === 0) {
      $modalInstance.close();
    }
    $scope.saving = false;
});
      });
    }
  };


  $scope.cancel = function() {
    $modalInstance.dismiss("cancel");
  };
});
