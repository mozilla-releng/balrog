/*global sweetAlert swal */
angular.module('app').controller('EditPermissionScheduledChangeCtrl',
function ($scope, $modalInstance, CSRF, Permissions, sc) {

  $scope.loading = true;

  $scope.original_sc = sc;
  $scope.sc = angular.copy(sc);
  if(sc.options){
    $scope.sc.options = JSON.stringify(sc.options);
  }
  $scope.currentItemTab = 1;
  $scope.is_edit = true;

  $scope.saving = false;




  $scope.updateScheduledPermission = function() {


    $scope.date = new Date();

    $scope.sc.when=$scope.date.getTime()+100;
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      Permissions.updateScheduledChange(sc.sc_id, $scope.sc, csrf_token)
      .success(function(response) {
        $scope.sc.sc_data_version = response.new_data_version;
        angular.copy($scope.sc, $scope.original_sc);
        $scope.saving = false;
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


  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
