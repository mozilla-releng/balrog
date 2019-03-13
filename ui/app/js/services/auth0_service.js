angular.module("app").factory('Auth0', function(angularAuth0) {
  var accessToken;
  var idToken;
  var expiresAt;
  var tokenRenewalTimeout;

  function scheduleRenewal() {
    var delay = expiresAt - Date.now();
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
    // Set the time that the access token will expire at
    expiresAt = (authResult.expiresIn * 1000) + new Date().getTime();
    accessToken = authResult.accessToken;
    idToken = authResult.idToken;
    scheduleRenewal();
  };
  var service = {
    login: function(path) {
      angularAuth0.authorize({"state": path});
    },
    logout: function() {
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("picture");
      accessToken = null;
      idToken = null;
      expiresAt = 0;
      clearTimeout(tokenRenewalTimeout);
    },
    getIdToken: function() {
      return idToken;
    },
    getAccessToken: function() {
      return accessToken;
    },
    getPicture: function() {
      return localStorage.getItem('picture');
    },
    isAuthenticated: function() {
      return localStorage.getItem('isLoggedIn') === 'true' && new Date().getTime() < expiresAt;
    },
    handleAuthentication: function(successCallback, errCallback) {
      angularAuth0.parseHash(function(err, authResult) {
        if (authResult && authResult.accessToken && authResult.idToken) {
          localLogin(authResult);
          if (successCallback) {
            successCallback(authResult.state);
          }
        }
        else if (err) {
          console.log(err);
          if (errCallback) {
            errCallback(err.error);
          }
        }
        else {
          if (errCallback) {
            errCallback("Couldn't complete login for unknown reason");
          }
        }
      });
    },
    renewTokens: function() {
      // TODO: this is getting a timeout error, only initial logins are working right now
      angularAuth0.checkSession({},
        function(err, result) {
          if (err) {
            console.log(err);
          } else {
            localLogin(result);
          }
        }
      );
    }
  };

  return service;
});
