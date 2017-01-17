angular.module("app").controller('RequiredSignoffsController',
function($scope, ProductRequiredSignoffs, PermissionsRequiredSignoffs) {
  $scope.loading = true;

  $scope.required_signoffs = {};
  $scope.selected_product = null;

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

    PermissionsRequiredSignoffs.getRequiredSignoffs()
    .success(function(response) {
      if (response["count"] > 0) {
        response["required_signoffs"].forEach(function(rs) {
          if (! (rs.product in $scope.required_signoffs)) {
            $scope.required_signoffs[rs.product] = {"permissions": {}};
          }
          else if (! ("permissions" in $scope.required_signoffs[rs.product])) {
            $scope.required_signoffs[rs.product]["permissions"] = {};
          }
        
          $scope.required_signoffs[rs.product]["permissions"][rs.role] = {
            "signoffs_required": rs.signoffs_required,
            "data_version": rs.data_version,
          };
        });
      }
    })
    // can a response be grabbed here?
    .error(function(response) {
      alert("error! " + response);
    });

    products = Object.keys($scope.required_signoffs);
    if (products.length > 0) {
      $scope.selected_product = products[0];
    }
  })
  // can a response be grabbed here?
  .error(function(response) {
    alert("error! " + response);
  })
  .finally(function() {
    $scope.loading = false;
  });
});
