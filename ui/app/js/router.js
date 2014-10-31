angular.module("app").config(function($routeProvider, $locationProvider) {

  $locationProvider.html5Mode(true);

  $routeProvider

  .when('/', {
    templateUrl: 'dashboard.html',
    controller: 'DashboardController'
  })

  .when('/permissions', {
    templateUrl: 'permissions.html',
    controller: 'PermissionsController',
    reloadOnSearch: false
  })

  .when('/permissions/:username', {
    templateUrl: 'permissions.html',
    controller: 'PermissionsController'
  })

  .when('/releases', {
    templateUrl: 'releases.html',
    controller: 'ReleasesController',
    reloadOnSearch: false
  })

  .when('/releases/:name', {
    templateUrl: 'releases.html',
    controller: 'ReleasesController',
    reloadOnSearch: false
  })

  .when('/rules', {
    templateUrl: 'rules.html',
    controller: 'RulesController',
    reloadOnSearch: false
  })

  .when('/rules/:id', {
    templateUrl: 'rules.html',
    controller: 'RulesController',
    reloadOnSearch: false
  })
  ;

  $routeProvider.otherwise({ redirectTo: '/' });

});
