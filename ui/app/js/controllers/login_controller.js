/*global: sweetAlert */

angular.module("app").controller('LoginController', function(angularAuth0) {
    // need to pass state here, maybe store it in localStorage?
    angularAuth0.popup.callback({"state": localStorage.getItem("pathBeforeLogin")});
});
