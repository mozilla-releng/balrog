angular.module("app").directive("rulefield", function() {
  return {
    restrict: "E",
    scope: {
      showdiff: "=",
      showsc: "=",
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
    }
  };
});
