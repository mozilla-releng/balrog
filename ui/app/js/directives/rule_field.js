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
      limittextto: "@",
    },
    templateUrl: "rule_field.html",
    link: function(scope, element, attr) {
      attr.$observe('limittextto', function(value) {
        scope.limittextto_sc = scope.limittextto;

        if(!value && scope.rule[scope.fieldname] !== null && scope.rule[scope.fieldname] !== undefined) {
          scope.limittextto = scope.rule[scope.fieldname].toString().length;
        }

        if(scope.rule.scheduled_change && scope.rule.scheduled_change[scope.fieldname] !== null && scope.rule.scheduled_change[scope.fieldname] !== undefined) {
            scope.limittextto_sc = scope.limittextto_sc ? scope.limittextto_sc : scope.rule.scheduled_change[scope.fieldname].toString().length;
        }
      });
    },
    controller: function($scope) {
      // For some reason directives don't inherit the Parent controller
      // so we need to explicit set this here.
      $scope.fieldIsChanging = fieldIsChanging;
    }
  };
});
