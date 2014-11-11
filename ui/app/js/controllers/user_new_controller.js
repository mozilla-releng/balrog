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
    $modalInstance.close($scope.user);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
