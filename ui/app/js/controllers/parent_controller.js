/*global: sweetAlert */

/* a middleware the sniffs on AJAX errors */
angular.module("app").factory('errorSniffer', ['$q', function($q) {
  return {
    responseError: function(rejection) {
      if (rejection.status === 401) {
        // Unauthorized
        sweetAlert("Unauthorized", rejection.data, "error");
      } else if (rejection.status === 500) {
        sweetAlert(
          "Internal Server Error",
          "An unexpected server error happened. See the console log for more details.",
          "error"
        );
        console.warn(rejection.status, rejection.data);
      } else if (rejection.status === 502) {
        sweetAlert(
          "Gateway Error (502)",
          "Seems we currently can't connect to the server.",
          "error"
        );
        console.warn(rejection.status, rejection.data);
      } else if (rejection.status === 404) {
        sweetAlert(
          "Page Not Found",
          "A resource was requested that can't be found\n" +
          "(" + rejection.config.method + " " + rejection.config.url + ")",
          "error"
        );
        // console.warn(rejection.status);
      }
      return $q.reject(rejection);
    }
  };
}]);

angular.module("app").config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('errorSniffer');
}]);


/* Put things in here that the sub-controllers can use */
angular.module("app").controller('ParentController',
function($scope, $window, $location, $http, Page, Auth0) {
  $scope.Page = Page;
  $scope.isEmpty = isEmpty;
  $scope.fieldIsChanging = fieldIsChanging;
  $scope.humanizeDate = humanizeDate;
  $scope.formatMoment = formatMoment;
  $scope.auth0 = Auth0;
  $scope.loc = $location;
  $scope.showAccessToken = function() {
    // This is a seemingly ridiculous chain of calls just to get a human readable date.
    // We need the moment(parseInt(...)) because Javascript's Date object won't parse
    // unix time as best I can tell, and moment won't take unix time in string form.
    // humanizeDate turns it into something more understandable for humans
    var expiresAt = localStorage.getItem("expiresAt");
    var accessToken = localStorage.getItem("accessToken");
    var validUntil = humanizeDate(moment(parseInt(expiresAt)));
    // This is also a kindof ridiculous chain of elements. SweetAlert only allows
    // one element in the content, so we need to create a single root element that contains
    // all the things we need in it. In our case, an <input> and <button> that shows/copies
    // the accessToken to the clipboard.
    var div = document.createElement("div");
    var input = document.createElement("input");
    var span = document.createElement("span");
    var button = document.createElement("button");
    var glyphicon = document.createElement("i");
    div.className = "input-group";
    input.className = "form-control";
    input.type = "text";
    input.value = accessToken;
    span.className = "input-group-btn";
    button.className = "btn";
    button.type = "button";
    button.title = "Copy to Clipboard";
    button.onclick = function() {
      input.select();
      navigator.clipboard.writeText(accessToken);
    };
    glyphicon.className = "glyphicon glyphicon-share";
    button.append(glyphicon);
    span.append(button);
    div.append(input);
    div.append(span);
    sweetAlert({
      title: "Your access token is valid until " + validUntil,
      content: {
        element: div,
      },
      icon: "info",
    });
  };
  function updateHttpDefaults() {
    $http.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("accessToken");
  }
  $scope.initiateLogin = function() {
    // Do the login in a new window, and set-up token renewal
    // when it completes.
    var loginWindow = $window.open('/auth0_login', '_blank');
    var timer = setInterval(function() {
      if (loginWindow.closed) {
        clearInterval(timer);
        $scope.$apply();
        if (Auth0.isAuthenticated()) {
          Auth0.scheduleRenewal(updateHttpDefaults);
          updateHttpDefaults();
        }
      }
    }, 500);
  };
});
