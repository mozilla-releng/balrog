angular.module("app").factory('Helpers', function() {
  var service = {
    replaceEmptyStrings: function(object) {
      for (var i in object) {
        if (object.hasOwnProperty(i)) {
          if ((typeof object[i] === 'string' || object[i] instanceof String) && object[i] === "") {
              object[i] = null;
          }
        }
      }
      return object;
    },
    selectPageSize: function($scope, controller_name){
      $scope.pageSize = $scope.page_size.id;
      localStorage.setItem(controller_name, JSON.stringify($scope.page_size));
    },
  };
  return service;
});
