angular.module("app").directive("tagInput", function() {
  return {
    restrict: "A",
    link: function(scope, element, attrs) {
      scope.$watch(attrs.ngModel, function(value) {
        if (value !== undefined) {
          var tempEl = $("<span>" + value + "</span>").appendTo("body");
          scope.inputWidth = tempEl.width() + 5;
          tempEl.remove();
        }
      });

      element.bind("keydown", function(event) {
        if (event.which === 9) {
          event.preventDefault();
        }
        if (event.which === 8) {
          scope.$apply(attrs.deleteTag);
        }
        if (event.which === 13){
          event.preventDefault();
        }
      });

      element.bind("keyup", function(event) {
        var key = event.which;
        if (key === 9 || key === 13) {
          event.preventDefault();
          scope.$apply(attrs.newTag);
        }
      });
    }
  };
});
