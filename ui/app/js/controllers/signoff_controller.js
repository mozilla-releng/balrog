angular.module('app').controller('SignoffCtrl',
function ($scope, $modalInstance, CSRF, title, service, sc_id, pk, details) {
  $scope.saving = false;
  $scope.title = title;
  $scope.sc_id = sc_id;
  $scope.pk = pk;
  $scope.details = details;
  $scope.selected_role = null;

  $scope.current_user_roles = ["blah", "foo", "crap"];

  $scope.$watch("user_roles", function() {
    if ($scope.selected_role === null) {
      var products = Object.keys($scope.user_roles);
      if (products.length > 0) {
        $scope.selected_role = products[0];
      }
    }
  }, true);

  $scope.saveChanges = function () {
    $scope.saving = true;
    CSRF.getToken()
    .then(function(csrf_token) {
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
