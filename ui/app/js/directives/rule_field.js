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
    }
  };
});
