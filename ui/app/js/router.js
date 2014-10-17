angular.module("app").config(function($routeProvider, $locationProvider) {

  $locationProvider.html5Mode(true);

  $routeProvider

  .when('/', {
    templateUrl: 'dashboard.html',
    controller: 'DashboardController'
  })

  .when('/rules', {
    templateUrl: 'rules.html',
    controller: 'RulesController'
  })

  .when('/rules/:id', {
    templateUrl: 'rules.html',
    controller: 'RulesController'
  })
  ;

  $routeProvider.otherwise({ redirectTo: '/' });

});
