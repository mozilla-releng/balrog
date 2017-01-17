angular.module("app").controller('RequiredSignoffsController',
function($scope, ProductRequiredSignoffs) {
  $scope.loading = true;

  $scope.required_signoffs = {};
  $scope.state = "current";

  ProductRequiredSignoffs.getRequiredSignoffs()
  .success(function(response) {
    if (response["count"] > 0) {
      response["required_signoffs"].forEach(function(rs) {
        if (! (rs.product in $scope.required_signoffs)) {
          $scope.required_signoffs[rs.product] = {"channels": {}};
        }
    
        if (! (rs.channel in $scope.required_signoffs[rs.product]["channels"])) {
          $scope.required_signoffs[rs.product]["channels"][rs.channel] = {};
        }
    
        $scope.required_signoffs[rs.product]["channels"][rs.channel][rs.role] = {
            "signoffs_required": rs.signoffs_required,
            "data_version": rs.data_version,
        };
      });
    }
  })
  // can a response be grabbed here?
  .error(function(response) {
  })
  .finally(function() {
    $scope.loading = false;
  });
});
