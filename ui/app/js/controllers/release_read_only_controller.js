angular.module('app').controller('ReleaseReadOnlyCtrl',
function ($scope, $modalInstance, CSRF, ReleasesReadonly, release) {
  $scope.loading = true;
  $scope.failed = false;
  $scope.saving = false;
  $scope.release = release;

  if(release.read_only) {
    ReleasesReadonly.getReleaseReadonly(release.name)
      .then(function(response) {
        $scope.release_readonly = response.data;
      })
      .finally(function () {
        $scope.loading = false;
      });
  }

  $scope.makeReadonly = function(csrf_token) {
    ReleasesReadonly.makeReadonly($scope.release.name, csrf_token)
      .success(function() {
        sweetAlert(
          'Release', 'Release was set to readonly successfully!', 'success');

        $scope.release.read_only = true;
        $modalInstance.close();
      })
      .error($scope.responseError)
      .finally($scope.operationComplete);
  };

  $scope.makeReadWrite = function(csrf_token) {
    ReleasesReadonly.makeReadWrite(
        $scope.release_readonly.release_name, $scope.release_readonly.data_version, csrf_token)
      .success(function() {
        sweetAlert(
          'Release', 'Release was set to modifiable successfully!', 'success');
        
        $scope.release.read_only = false;
        $modalInstance.close();
      })
      .error($scope.responseError)
      .finally($scope.operationComplete);
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

  $scope.operationComplete = function () {
    $scope.saving = false;
  };

  $scope.saveChanges = function () {
    $scope.saving = true;

    CSRF.getToken()
      .then(function(csrf_token) {
        if($scope.release.read_only) {
          $scope.makeReadWrite(csrf_token);
        } else {
          $scope.makeReadonly(csrf_token);
        }
    });
  };

  $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
  };
});
