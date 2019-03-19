/*global: sweetAlert */

angular.module("app").controller('Auth0LoginController', function(Auth0) {
    // have to pass some sort of state, otherwise auth0 sets something that we don't know the value of!
    Auth0.login("fakestate");
});

