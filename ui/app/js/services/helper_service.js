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
    numberValidator: function (validation_fields) {
      var validation_results = {};
      for (var key in validation_fields) {
        var value = validation_fields[key];
        if (isNaN(value)) {
          validation_results[key] = 'Value must be a number';
          continue;
        }
        // Filter negative numbers and maximum, if specified.
        if (value < 0) {
          validation_results[key] = 'Value must be a positive number';
        } else if (key === 'rate' && value > 100) {
          validation_results[key] = 'Value should not be more than 100';
        } else {
          validation_results[key] = false;
        }
      }
      return validation_results;
    },
  };
  return service;
});
