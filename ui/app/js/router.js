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

  .when("/releases/scheduled_changes", {
    templateUrl: "release_scheduled_changes.html",
    controller: "ReleaseScheduledChangesController",
    reloadOnSearch: false
  })

  .when("/scheduled_changes/releases/:sc_id", {
    templateUrl: "release_scheduled_changes.html",
    controller: "ReleaseScheduledChangesController",
    reloadOnSearch: false
  })

  .when('/releases/:name', {
    templateUrl: 'releases.html',
    controller: 'ReleasesController',
    reloadOnSearch: false
  })

  .when("/rules/scheduled_changes", {
    templateUrl: "rule_scheduled_changes.html",
    controller: "RuleScheduledChangesController",
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
