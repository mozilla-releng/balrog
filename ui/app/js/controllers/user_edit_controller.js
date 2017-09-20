/*global sweetAlert swal */
angular.module('app').controller('UserPermissionsCtrl',
function ($scope, $modalInstance, CSRF, Permissions, users, is_edit, user) {

  $scope.loading = true;
  $scope.users = users;
  $scope.currentItemTab = 1;

  var allPermissions = {
        "admin": ["products"],
        "release": ["actions", "products"],
        "release_locale": ["actions", "products"],
        "release_read_only": ["actions", "products"],
        "rule": ["actions", "products"],
        "permission": ["actions"],
        "required_signoff": ["products"],
        "scheduled_change": ["actions"],
    };

  $scope.onPermission = function(){
      $scope.available_options = allPermissions[$scope.permission.permission];
  }
  $scope.selected_options = [];
  $scope.toggleOption = function(option){
      if($scope.selected_options.indexOf(option) !== -1){
          $scope.selected_options.splice($scope.selected_options.indexOf(option), 1);
      }else{
          $scope.selected_options.push(option);
      }
  };
  $scope.is_edit = is_edit;
  $scope.permission = {
    permission: '',
    options_as_json: ''
  };
  $scope.errors = {
    permissions: {}
  };
  if($scope.is_edit){
    $scope.original_user = user;
    $scope.user = angular.copy(user);
    $scope.user.permissions = [];
    Permissions.getUserPermissions($scope.user.username)
    .then(function(permissions) {
      _.forEach(permissions, function(p) {
        if (p.options) {
          p.options_as_json = JSON.stringify(p['options']);
        }
      });
  
      $scope.user.permissions = permissions;
    });

    $scope.user.roles = [];
    Permissions.getUserRoles($scope.user.username)
    .success(function(response) {
      $scope.user.roles = response.roles;
    })
    .error(function(response) {
      if (typeof response === 'object') {
        $scope.errors = response;
        sweetAlert(
          "Failed to load User Roles",
          "error"
        );
      } else if (typeof response === 'string') {
        sweetAlert(
          "Failed to load User Roles" +
          "(" + response+ ")",
          "error"
        );
      }
    })
    .finally(function() {
      $scope.loading = false;
    });
  }
  else {
    $scope.user = {
      username: '',
    };
    $scope.loading = false;
    $scope.user.permissions = [];
    $scope.user.roles = [];
  }
  

  $scope.roles_list = [];
  Permissions.getAllRoles()
  .success(function(response) {
    $scope.roles_list = response.roles;
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
  });

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
    // $scope.permission.options = $scope.permission.options_as_json;
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
              "This persmission has already been granted",
              "error"
            );
          }
          else{
            sweetAlert(
              "Form submission error",
              "Persmissions must be selected",
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
