/*global sweetAlert swal */
angular.module('app').controller('NewPermissionScheduledChangeCtrl',
function ($scope, $modalInstance, CSRF, Permissions, scheduled_changes, sc) {

  $scope.loading = true;
  $scope.scheduled_changes = scheduled_changes;
  $scope.scheduledpermissions = [];
  $scope.currentItemTab = 1;
  $scope.is_edit = true;
  $scope.sc = angular.copy(sc);
  $scope.permission = {
    permission: '',
    options: ''
  };
  $scope.errors = {
    permissions: {}
  };

  $scope.sc.permissions = [];
  Permissions.getUserPermissions(sc.username)
  .then(function(permissions) {
    _.forEach(permissions, function(p) {
      if (p.options) {
        p.options = JSON.stringify(p['options']);
      }
    });
    $scope.sc.permissions = permissions;
    // console.log('$scope.sc.permissions');
    // console.dbg($scope.sc.permissions);
    $scope.loading = false;
  });


  $scope.saving = false;




  $scope.addScheduledPermission = function() {
  if($scope.permission.permission) {

    date = new Date();

    permission_sc = angular.copy($scope.sc);
    permission_sc.permission = $scope.permission.permission;
    permission_sc.data_version = $scope.permission.data_version;
    permission_sc.options = $scope.permission.options;
    permission_sc.when=date.getTime()+100;
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.addScheduledChange(permission_sc, csrf_token)
      .success(function(response) {
        $scope.sc.sc_data_version = 1;
        $scope.sc.sc_id = response.sc_id;
        $scope.scheduled_changes.push($scope.sc);
        $modalInstance.close();
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

     $scope.permission = {
          permission: '',
          options: ''
        };
    }
  };

  $scope.addScheduledUser = function() {


    date = new Date();

    $scope.permission.when = date.getTime()+100;
    $scope.permission.change_type = "insert";
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.addScheduledChange($scope.permission, csrf_token)
      .success(function(response) {
        $scope.sc.sc_data_version = 1;
        $scope.sc.sc_id = response.sc_id;
        $scope.scheduled_changes.push($scope.permission);
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

   $scope.scheduledUpdatePermission = function(permission) {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      date = new Date();
      permission.when = date.getTime()+100;
      permission.username = $scope.sc.username;
      permission.change_type = "update";
      Permissions.addScheduledChange(permission, csrf_token)
      .success(function(response) {
        permission.data_version = response.new_data_version;
        $scope.errors = {
            permissions: {}
        };
        sweetAlert("Permission Scheduled for Update", "success");
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

   $scope.scheduledDeletePermission = function(permission) {
    sweetAlert({
      title: "Are you sure?",
      text: "This will scheduled delete for the permission.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, delete it!",
      closeOnConfirm: false
    }, function(){
      $scope.saving = true;
      date = new Date();
      permission.when = date.getTime()+100;
      permission.change_type = "delete";
      permission.username = $scope.sc.username;
      CSRF.getToken()
      .then(function(csrf_token) {
        Permissions.addScheduledChange(permission, csrf_token)
        .success(function(response) {
          $scope.sc.permissions.splice($scope.sc.permissions.indexOf(permission), 1);
          sweetAlert("Permission Scheduled For Deletion.", "success");
          $scope.cancel();
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

    });

  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
