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
    addErrorFields: function (error_object) {
      // method to add to the $scope.errors object with {field: field error} if the fields are present in the error details.
      var error_details = error_object.detail;
      var fields = ['priority', 'backgroundRate', 'mapping', 'channel', 'product', 'fallbackMapping', 'alias',
        'product', 'version', 'buildID', 'locale', 'distribution', 'buildTarget', 'osVersion', 'instructionSet',
        'memory', 'distVersion', 'comment', 'update_type', 'headerArchitecture', 'telemetry_product',
        'telemetry_channel', 'telemetry_uptake'];
      if (error_details) {
        for (var x = 0; x < fields.length; x++) {
          if (error_details.indexOf(fields[x]) >= 0) {
            error_object[fields[x]] = error_details;
          }
        }
      }
    },
  };
  return service;
});
