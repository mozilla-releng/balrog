angular.module("app").directive("scrulefield", function() {
  return {
    restrict: "E",
    scope: {
      rule: "=",
      fieldname: "@",
      fieldtitle: "@",
      help: "@",
    },
    templateUrl: "rule_field.html",
    controller: function($scope) {
      // For some reason directives don't inherit the Parent controller
      // so we need to explicit set this here.
      $scope.fieldIsChanging = fieldIsChanging;
      $scope.showdiff = true;
      $scope.showsc = true;
    }
  };
});
