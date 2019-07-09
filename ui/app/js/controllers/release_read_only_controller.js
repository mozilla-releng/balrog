angular.module('app').controller('ReleaseReadOnlyCtrl',
function ($scope, $modalInstance, CSRF, Releases, release) {

  $scope.release = release;
  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRF.getToken()
    .then(function(csrf_token) {
      var data = angular.copy($scope.release);
      data.read_only = release.read_only ? "" : true;

      if ($scope.changeRequiresSignoffs()) {
        $scope.scheduleReadWriteReleaseChange(data, csrf_token);
      } else {
        $scope.changeReadOnly(data, csrf_token);
      }
    });
  };

  $scope.changeReadOnly = function(release, csrf_token) {
    Releases.changeReadOnly(release.name, release, csrf_token)
    .success(function(response) {
      $scope.release.data_version = response.new_data_version;
      $scope.release.read_only = release.read_only;
      $modalInstance.close();
    })
    .error($scope.responseError)
    .finally($scope.operationComplete);
  };

  $scope.scheduleReadWriteReleaseChange = function(release, csrf_token) {
    var when = new Date();
    when.setSeconds(when.getSeconds() + 10);

    var sc = {
      change_type: 'update',
      name: release.name,
      product: release.product,
      read_only: false,
      when: when,
      data_version: release.data_version
    };

    Releases.addScheduledChange(sc, csrf_token)
      .success(function(response) {
        sc.sc_data_version = 1;
        sc.sc_id = response.sc_id;
        $scope.release.sc = sc;
        sweetAlert(
          'Release', 'Release was scheduled to be modifiable successfully!', 'success');
        $modalInstance.close();
      })
      .error($scope.responseError)
      .finally($scope.operationComplete);
  };

  $scope.operationComplete = function () {
    $scope.saving = false;
  };

  $scope.responseError = function(response) {
    if (typeof response === 'object') {
      $scope.errors = response;
      sweetAlert(
        'Form submission error',
        'See fields highlighted in red.',
        'error'
      );
    }
  };

  $scope.changeRequiresSignoffs = function() {
    return $scope.release.read_only &&
      $scope.release.required_signoffs &&
      $scope.release.required_signoffs.length > 0;
  };

  $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
  };
});
