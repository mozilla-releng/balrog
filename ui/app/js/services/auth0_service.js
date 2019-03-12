angular.module("app").factory('Auth0', function(angularAuth0) {
  var accessToken;
  var idToken;

  localLogin = function(authResult) {
    // Set isLoggedIn flag in localStorage
    localStorage.setItem('isLoggedIn', true);
    localStorage.setItem('accessToken', authResult.accessToken);
    localStorage.setItem('picture', authResult.idTokenPayload.picture);
    // Set the time that the access token will expire at
    expiresAt = (authResult.expiresIn * 1000) + new Date().getTime();
    accessToken = authResult.accessToken;
    idToken = authResult.idToken;
  };
  var service = {
    login: function(path) {
      angularAuth0.authorize({"state": path});
    },
    logout: function() {
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("accessToken");
      accessToken = null;
      idToken = null;
      picture = null;
      expiresAt = null;
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
    handleAuthentication: function(successCallback, errCallback) {
      angularAuth0.parseHash(function(err, authResult) {
        if (authResult && authResult.accessToken && authResult.idToken) {
          localLogin(authResult);
          successCallback(authResult.state);
        }
        else if (err) {
          errCallback(err.error);
        }
        else {
          errCallback("Couldn't complete login for unknown reason");
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
