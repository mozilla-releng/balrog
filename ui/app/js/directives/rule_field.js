/*global: moment */

angular.module("app").directive("rulefield", function() {
  return {
    restrict: "E",
    scope: {
      showsc: "@",
      rule: "@",
      fieldname: "@",
      fieldtitle: "@",
    },
    templateUrl: "rule_field.html",
    controller: function($scope) {
      $scope.sc = $scope.rule.scheduled_change;
      $scope.showsc = ($scope.showsc === 'true');
      $scope.showsc = true;
      console.log($scope);
    }
  };
});
