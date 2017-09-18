/*global sweetAlert swal */
angular.module('app').controller('NewPermissionScheduledChangeCtrl',
function ($scope, $modalInstance, CSRF, Permissions, scheduled_changes, sc) {

  $scope.loading = true;
  $scope.scheduled_changes = scheduled_changes;
  $scope.currentItemTab = 1;
  $scope.is_edit = true;
  $scope.saving = false;
  $scope.sc = angular.copy(sc);
  $scope.permission = {
    permission: '',
    options: ''
  };
  $scope.errors = {
    permissions: {}
  };
  $scope.permissions_list = [
    {value : "", name : "---Please select---"},
    {value : "admin", name : "Admin"},
    {value : "rule", name : "Rule"},
    {value : "release", name : "Release"},
    {value : "release_read_only", name : "Release Read Only"},
    {value : "release_locale", name : "Release Locale"},
    {value : "required_signoff", name : "Required Signoff"},
    {value : "permission", name : "Permission"},
    {value : "scheduled_change", name : "Scheduled Change"},
  ];


  $scope.sc.permissions = [];
  Permissions.getUserPermissions(sc.username)
  .then(function(permissions) {
    _.forEach(permissions, function(p) {
      if (p.options) {
        p.options = JSON.stringify(p['options']);
      }
    });
    $scope.sc.permissions = permissions;
    $scope.loading = false;
  });


  $scope.addScheduledPermission = function() {
    date = new Date();
    permission_sc = angular.copy($scope.permission);
    permission_sc.when = date.getTime() + 5000;
    permission_sc.change_type = "insert";
    $scope.saving = true;
    if($scope.sc.username) {
    permission_sc.username = $scope.sc.username;
    }
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.addScheduledChange(permission_sc, csrf_token)
      .success(function(response) {
        permission_sc.sc_data_version = 1;
        permission_sc.sc_id = response.sc_id;
        sweetAlert("Saved", "Permission Scheduled", "success");
        if(permission_sc.options){
          permission_sc.options = JSON.parse(permission_sc.options);
        }
        $scope.scheduled_changes.push(permission_sc);
        if($scope.sc.username) {
        sweetAlert("Permission Scheduled", "success");
        }
        else {
        $modalInstance.close();
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

     $scope.permission = {
          permission: '',
          options: ''
        };
  };



  $scope.scheduledUpdatePermission = function(permission) {
    $scope.saving = true;

    CSRF.getToken()
    .then(function(csrf_token) {
      date = new Date();
      permission.when = date.getTime() + 5000;
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
      permission.when = date.getTime()+5000;
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
