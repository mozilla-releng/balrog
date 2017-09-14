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
      $scope.fieldIsChanging = fieldIsChanging;
    }
  };
});
