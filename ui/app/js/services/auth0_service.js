angular.module("app").factory('Auth0', function(angularAuth0, $http) {
  var tokenRenewalTimeout;

  function renewTokens(errCallback) {
    angularAuth0.checkSession({},
      function(err, result) {
        if (err) {
          if (errCallback) {
            errCallback(err.error_description);
          }
        } else {
          localLogin(result);
        }
      }
    );
  }
  function scheduleRenewal() {
    // Renew tokens 5 minutes ahead of expiration
    var delay = localStorage.getItem("expiresAt") - Date.now() - 300000;
    if (delay > 0) {
      tokenRenewalTimeout = setTimeout(function() {
        renewTokens();
      }, delay);
    }
  }

  localLogin = function(authResult) {
    // Set isLoggedIn flag in localStorage
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('accessToken', authResult.accessToken);
    localStorage.setItem('picture', authResult.idTokenPayload.picture);
    localStorage.setItem('username', authResult.idTokenPayload.email);
    // Set the time that the access token will expire at
    localStorage.setItem('expiresAt', authResult.expiresIn * 1000 + new Date().getTime());
    scheduleRenewal();
    $http.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("accessToken");
  };
  var service = {
    login: function(state) {
      angularAuth0.authorize({"state": state});
    },
    logout: function() {
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("picture");
      localStorage.removeItem("username");
      localStorage.removeItem("expiresAt");
      clearTimeout(tokenRenewalTimeout);
    },
    getPicture: function() {
      return localStorage.getItem('picture');
    },
    isAuthenticated: function() {
      return localStorage.getItem('isLoggedIn') === 'true' && new Date().getTime() < localStorage.getItem('expiresAt');
    },
    handleAuthentication: function(state, successCallback, errCallback) {
      angularAuth0.parseHash({"state": state}, function(err, authResult) {
        if (authResult && authResult.accessToken && authResult.idToken) {
          localLogin(authResult);
          successCallback();
        }
        else if (err) {
          if (errCallback) {
            errCallback(err.errorDescription);
          }
        }
        else {
          if (errCallback) {
            errCallback("unknown error");
          }
        }
      });
    },
    renewTokens: renewTokens,
    scheduleRenewal: scheduleRenewal
  };

  return service;
});
