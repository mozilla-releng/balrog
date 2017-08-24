/*global: moment */

angular.module("app").directive("rulefield", function() {
  return {
    restrict: "E",
    scope: {
      showsc: "=",
      rule: "=",
      fieldname: "@",
      fieldtitle: "@",
      help: "@",
    },
    templateUrl: "rule_field.html",
    controller: function($scope) {
      $scope.sc = $scope.rule.scheduled_change;
      $scope.fieldvalue = null;
      if ($scope.rule[$scope.fieldname] !== null && $scope.rule[$scope.fieldname] !== undefined) {
        $scope.fieldvalue = $scope.rule[$scope.fieldname];
        if ($scope.fieldvalue === true) {
          $scope.fieldvalue = "Yes";
        }
        if ($scope.fieldvalue === false) {
          $scope.fieldvalue = "No";
        }
      }
      $scope.scvalue = null;
      if ($scope.sc !== null && $scope.sc[$scope.fieldname] !== null && $scope.sc[$scope.fieldname] !== undefined) {
        $scope.scvalue = $scope.sc[$scope.fieldname];
        if ($scope.sc[$scope.fieldname] === true) {
          $scope.scvalue = "Yes";
        }
        if ($scope.sc[$scope.fieldname] === false) {
          $scope.scvalue = "No";
        }
      }
    }
  };
});
