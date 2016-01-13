/*global sweetAlert swal */
angular.module('app').controller('UserPermissionsCtrl',
function ($scope, $modalInstance, CSRF, Permissions, user, users) {

  $scope.loading = true;
  $scope.users = users;

  $scope.is_edit = true;
  $scope.original_user = user;
  $scope.user = angular.copy(user);
  $scope.permission = {
    permission: '',
    options_as_json: ''
  };
  $scope.errors = {
    permissions: {}
  };

  $scope.user.permissions = [];
  Permissions.getUserPermissions(user.username)
  .then(function(permissions) {
    _.forEach(permissions, function(p) {
      if (p.options) {
        p.options_as_json = JSON.stringify(p['options']);
      }
    });

    $scope.user.permissions = permissions;
    // console.log('$scope.user.permissions');
    // console.dbg($scope.user.permissions);
    $scope.loading = false;
  });

  $scope.saving = false;

  $scope.$watchCollection('permission', function(value) {
    value.options = value.options_as_json;
  });

  $scope.addPermission = function() {
    // $scope.permission.options = $scope.permission.options_as_json;
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.addPermission($scope.user.username, $scope.permission, csrf_token)

      .success(function(response) {
        $scope.permission.data_version = response.new_data_version;
        $scope.user.permissions.push($scope.permission);
        // reset the add form
        $scope.permission = {
          permission: '',
          options_as_json: ''
        };
        $scope.errors = {
          permissions: {}
        };
        sweetAlert("Saved", "Permission added.", "success");
      })
      .error(function(response) {
        if (typeof response === 'object') {
          $scope.errors = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        } else if (typeof response === 'string') {
          // quite possibly an error in the blob validation
          sweetAlert(
            "Form submission error",
            "Unable to submit successfully.\n" +
            "(" + response+ ")",
            "error"
          );
        }
      })
      .finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.deletePermission = function(permission) {
    sweetAlert({
      title: "Are you sure?",
      text: "This will delete the permission.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, delete it!",
      closeOnConfirm: false
    }, function(){
      $scope.saving = true;
      CSRF.getToken()
      .then(function(csrf_token) {
        Permissions.deletePermission($scope.user.username, permission, csrf_token)
        .success(function(response) {
          $scope.user.permissions.splice($scope.user.permissions.indexOf(permission), 1);
          sweetAlert("Deleted", "Permission deleted.", "success");
          if (!$scope.user.permissions.length) {
            var index = null;
            _.each($scope.users, function(user, i) {
              if (user.username === $scope.user.username) {
                index = i;
              }
            });
            $scope.users.splice(index, 1);
          }
          $scope.cancel();
        })
        .error(function(response) {
          console.error(response);
        })
        .finally(function() {
          $scope.saving = false;
        });
      });

    });

  };

  $scope.updatePermission = function(permission) {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      permission.options = permission.options_as_json;
      Permissions.updatePermission($scope.user.username, permission, csrf_token)
      .success(function(response) {
        permission.data_version = response.new_data_version;
        $scope.errors = {
            permissions: {}
        };
        sweetAlert("Saved", "Permission changes saved.", "success");
      })
      .error(function(response) {
        if (typeof response === 'object') {
          $scope.errors.permissions[permission.permission] = response;
          sweetAlert(
            "Form submission error",
            "See fields highlighted in red.",
            "error"
          );
        } else if (typeof response === 'string') {
          // quite possibly an error in the blob validation
          sweetAlert(
            "Form submission error",
            "Unable to submit successfully.\n" +
            "(" + response+ ")",
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
