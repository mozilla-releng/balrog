// angular.module('app').controller('UserDeleteCtrl',
// function ($scope, $modalInstance, CSRFService, Permissions, user, users) {
//
//   $scope.user = user;
//   $scope.users = users;
//   $scope.saving = false;
//
//   $scope.saveChanges = function () {
//     $scope.saving = true;
//     CSRFService.getToken()
//     .then(function(csrf_token) {
//       Permissions.deleteUser($scope.user.id, $scope.user, csrf_token)
//       .success(function(response) {
//         $scope.users.splice($scope.users.indexOf($scope.user), 1);
//         $modalInstance.close();
//       })
//       .error(function() {
//         console.error(arguments);
//       })
//       .finally(function() {
//         $scope.saving = false;
//       });
//     });
//   };
//
//   $scope.cancel = function () {
//     $modalInstance.dismiss('cancel');
//   };
// });
