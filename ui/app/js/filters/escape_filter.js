angular.module("app").filter("uriencode", function() {
    return window.encodeURIComponent;
});
