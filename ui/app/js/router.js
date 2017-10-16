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

  .when('/permissions/scheduled_changes', {
    templateUrl: "permission_scheduled_changes.html",
    controller: "PermissionScheduledChangesController",
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

  .when("/scheduled_changes/rules/:sc_id", {
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
    
  .when('/required_signoffs', {
    templateUrl: 'required_signoffs.html',
    controller: 'RequiredSignoffsController',
    reloadOnSearch: false
  })

  .when('/history', {
    templateUrl: 'history.html',
    controller: 'HistoryController',
    reloadOnSearch: false
  })

  ;

  $routeProvider.otherwise({ redirectTo: '/' });

});
