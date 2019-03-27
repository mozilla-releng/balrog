if (typeof angular !== 'object') {
  throw new Error('Angular must be loaded.');
}

if (!angular.isObject(auth0)) {
  throw new Error('Auth0 must be loaded.');
}

angular.module('auth0.auth0', []).provider('angularAuth0', angularAuth0);

function angularAuth0() {
  this.init = function(config) {
    if (!config) {
      throw new Error('Client ID and Domain are required to initialize Auth0.js');
    }
    this.config = config;
  };

  this.$get = [
    '$rootScope',
    function($rootScope) {
      var Auth0Js = new auth0.WebAuth(this.config);
      var webAuth = {};
      var functions = [];

      for (var i in Auth0Js) {
        if (angular.isFunction(Auth0Js[i])) {
          functions.push(i);
        }
        if (angular.isObject(Auth0Js[i])) {
          webAuth[i] = Auth0Js[i];
        }
      }

      function wrapArguments(parameters) {
        var lastIndex = parameters.length - 1,
          func = parameters[lastIndex];
        if (angular.isFunction(func)) {
          parameters[lastIndex] = function() {
            var args = arguments;
            $rootScope.$evalAsync(function() {
              func.apply(Auth0Js, args);
            });
          };
        }
        return parameters;
      }

      for (var i = 0; i < functions.length; i++) {
        webAuth[functions[i]] = (function(name) {
          var customFunction = function() {
            return Auth0Js[name].apply(Auth0Js, wrapArguments(arguments));
          };
          return customFunction;
        })(functions[i]);
      }

      return webAuth;
    }
  ];
}
