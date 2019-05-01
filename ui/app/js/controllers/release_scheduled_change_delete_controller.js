angular.module("app").controller("DeleteReleaseScheduledChangeCtrl",
function ($scope, $modalInstance, CSRF, service, object_name, sc, scheduled_changes) {

  $scope.sc = sc;
  $scope.object_name = object_name;
  $scope.scheduled_changes = scheduled_changes;
  $scope.saving = false;
  $scope.formatMoment = formatMoment;

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
      service.deleteScheduledChange($scope.sc.sc_id, $scope.sc, csrf_token)
      .success(function(response) {
        $scope.scheduled_changes.splice($scope.scheduled_changes.indexOf($scope.sc), 1);
        $modalInstance.close();
      })
      .error(function(response) {
        if (typeof response === 'object') {
          sweetAlert(
            {
              title: "Form submission error",
              text: response.exception
            },
            function() { $scope.cancel(); }
          );
        }
      })
      .finally(function() {
        $scope.saving = false;
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss("cancel");
  };
});
