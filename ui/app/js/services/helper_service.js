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
    integerValidator: function (validation_fields) {
      var validation_results = {};
      for (var key in validation_fields) {
        var value = validation_fields[key];
        if (isNaN(value)) {
          validation_results[key] = key + ' field value must be an integer. "' + value + '" is not an integer.';
          continue;
        }
        // Filter negative numbers and maximum, if specified.
        if (value < 0) {
          validation_results[key] = key + ' field value should be an integer >= 0 '+ key +': '+ value +' is not a "'+ key +'"';
        } else if (key === 'backgroundRate' && value > 100) {
          validation_results[key] = 'backgroundRate field value should be an integer <= 100 backgroundRate: '+ value + ' is not a "backgroundRate"';
        } else {
          validation_results[key] = false;
        }
      }
      return validation_results;
    },
    replaceChar: function(input, searchvalue, newvalue) {
        var re = new RegExp(searchvalue, "g");
        return input.replace(re, newvalue);
    },
  };
  return service;
});
