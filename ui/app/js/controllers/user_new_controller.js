angular.module('app').controller('NewUserCtrl',
function($scope, $http, $modalInstance, CSRF, Permissions, users) {

  $scope.is_edit = false;
  $scope.users = users;
  $scope.user = {
    username: '',
  };
  $scope.errors = {};
  $scope.saving = false;

  $scope.saveChanges = function () {
    if (!$scope.user.username) {
        $scope.errors.nullValue = 'The username field cannot be empty';
        sweetAlert("failed", $scope.errors.nullValue, "error");
        return false;
    }
    $modalInstance.close($scope.user);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
