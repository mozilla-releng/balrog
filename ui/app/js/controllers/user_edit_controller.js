/*global sweetAlert swal */
angular.module('app').controller('UserPermissionsCtrl',
function ($scope, $modalInstance, CSRF, Permissions, users, roles, is_edit, user, permissionSignoffRequirements) {

  $scope.loading = true;
  $scope.users = users;
  $scope.roles_list = roles;
  $scope.originalPermissions = [];

  $scope.currentItemTab = 1;

  $scope.is_edit = is_edit;
  $scope.permission = {
    permission: '',
    options_as_json: ''
  };
  $scope.errors = {
    permissions: {}
  };

  if ($scope.is_edit) {
    $scope.original_user = user;
    $scope.user = angular.copy(user);

    $scope.user.permissions = [];
    Permissions.getUserInfo($scope.user.username)
      .then(function (response) {
        _.forEach(response.permissions, function (p) {
          if (p.options) {
            p.options_as_json = JSON.stringify(p['options']);
          }
        });
        $scope.originalPermissions = angular.copy(response.permissions);
        $scope.user.permissions = response.permissions;
      });

    $scope.users.forEach(function (eachUser) {
      if (eachUser.username === $scope.user.username) {
        $scope.user.roles = eachUser.roles;
      }
    });
    $scope.loading = false;

  }
  else {
    $scope.user = {
      username: '',
    };
    $scope.loading = false;
    $scope.user.permissions = [];
    $scope.user.roles = [];
  }


  function fromFormData(permission) {
    permission = angular.copy(permission);
    try {
      permission.options = permission.options_as_json && JSON.parse(permission.options_as_json);
    } catch(e) {
      // No options, I guess
    }
    return permission;
  }

  function permissionSignoffsRequired(currentPermission, newPermission) {
    if (currentPermission) {
      currentPermission = fromFormData(currentPermission);
    }
    if (newPermission) {
      newPermission = fromFormData(newPermission);
    }
    return Permissions.permissionSignoffsRequired(currentPermission, newPermission, permissionSignoffRequirements);
  }
  $scope.$watch("permission", function(permission) {
    $scope.permissionSignoffsRequired = permissionSignoffsRequired(permission);
  }, true);
  $scope.userPermissionsSignoffRequirements = [];
  $scope.$watch("user.permissions", function(permissions) {
    $scope.userPermissionsSignoffRequirements = permissions.map(function(permission, i) {
      return {
        signoffRequirements: permissionSignoffsRequired($scope.originalPermissions[i], permission),
        deleteSignoffRequirements: permissionSignoffsRequired($scope.originalPermissions[i])
      };
    });
  }, true);


  $scope.saving = false;
  $scope.usersaved = false;

  $scope.showRow = function () {
    return $scope.usersaved || $scope.is_edit;
  };

  $scope.$watchCollection('permission', function(value) {
    value.options = value.options_as_json;
  });
  $scope.grantRole = function() {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.grantRole($scope.user.username, $scope.role.role, $scope.role.data_version, csrf_token)
      .success(function(response) {
        $scope.role.data_version = response.new_data_version;
        $scope.user.roles.push($scope.role);
        if (!($scope.role.role in $scope.roles_list)) {
          $scope.roles_list.push($scope.role.role);
        }
        // reset the add form
        $scope.role = {
          role: '',
          data_version: ''
        };
        sweetAlert("Saved", "Role granted.", "success");
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

  $scope.addPermission = function() {
    $scope.permission.options = $scope.permission.options_as_json;
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      if (!$scope.user.username) {
        $scope.errors.nullValue = 'The username field cannot be empty';
        sweetAlert("failed", $scope.errors.nullValue, "error");
        $scope.saving = false;
        return false;
      }
      Permissions.addPermission($scope.user.username, $scope.permission, csrf_token)
      .success(function(response) {
        if ($scope.user.permissions){
          $scope.users.push($scope.user);
          $scope.permission.data_version = response.new_data_version;
          $scope.originalPermissions.push(angular.copy($scope.permission));
          $scope.user.permissions.push($scope.permission);
          // reset the add form
          $scope.permission = {
            permission: '',
            options_as_json: ''
          };
          $scope.errors = {
            permissions: {}
          };
          $scope.usersaved = true;
          sweetAlert("Saved", "Permission added.", "success");
        }
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

  $scope.revokeRole = function(role) {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.revokeRole($scope.user.username, role, csrf_token)
      .success(function(response) {
        $scope.user.roles.splice($scope.user.roles.indexOf(role), 1);
        sweetAlert("Deleted", "Role deleted.", "success");
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
    $scope.saving = false;
  };

  $scope.updatePermission = function(permission) {
    $scope.saving = true;
    $scope.usersaved = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      permission.options = permission.options_as_json;
      Permissions.updatePermission($scope.user.username, permission, csrf_token)
      .success(function(response) {
        permission.data_version = response.new_data_version;
        $scope.originalPermissions.push(angular.copy($scope.permission));
        $scope.user.permissions.push($scope.permission);
        $scope.permission = {
          permission: '',
          options_as_json: ''
        };
        $scope.errors = {
            permissions: {}
        };
        sweetAlert("Saved", "Permission changes saved.", "success");
      })
      .error(function(response) {
        if (typeof response === 'object') {
          $scope.errors.permissions[permission.permission] = response;
          var permission_found = $scope.user.permissions.filter(function(permission) {
            return (permission.permission === $scope.permission.permission);
          });
          if(permission_found.length){
            sweetAlert(
              "Form submission error",
              "This permission has already been granted",
              "error"
            );
          }
          else{
            sweetAlert(
              "Form submission error",
              "Permissions must be selected",
              "error"
            );
          }
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
