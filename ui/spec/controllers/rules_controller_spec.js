describe("controller: RulesController", function() {
  //https://stackoverflow.com/questions/38721298/jasmine-karma-array-find-is-not-a-function
  if (typeof Array.prototype.find !== 'function') {
    Array.prototype.find = function(iterator) {
      var list = Object(this);
      var length = list.length >>> 0;
      var thisArg = arguments[1];
      var value;

      for (var i = 0; i < length; i++) {
          value = list[i];
          if (iterator.call(thisArg, value, i, list)) {
              return value;
          }
      }
      return undefined;
    };
  }

  beforeEach(function() {
    module("app");
  });

  var sample_rules = {
    "count": 55,
    "rules": [
      {
        "comment": "Comment",
        "product": null,
        "buildID": null,
        "backgroundRate": 100,
        "mapping": "No-Update",
        "fallbackMapping": null,
        "rule_id": 19,
        "priority": 1,
        "data_version": 9,
        "version": null,
        "headerArchitecture": null,
        "update_type": "minor",
        "buildTarget": null,
        "locale": null,
        "osVersion": null,
        "instructionSet": null,
        "memory": null,
        "distribution": null,
        "channel": "nightly",
        "alias": null,
        "distVersion": null,
        "whitelist": null,
        "scheduled_change": null
    },
    {
        "comment": null,
        "product": "GMP",
        "buildID": null,
        "backgroundRate": 100,
        "mapping": "GMP-Firefox33-201410010830",
        "fallbackMapping": null,
        "rule_id": 67,
        "priority": 10,
        "data_version": 2,
        "version": ">=33.0",
        "headerArchitecture": null,
        "update_type": "minor",
        "buildTarget": null,
        "locale": null,
        "osVersion": null,
        "instructionSet": null,
        "memory": null,
        "distribution": null,
        "channel": null,
        "alias": null,
        "distVersion": null,
        "whitelist": null,
        "scheduled_change": null
    }
    ]
  };

  beforeEach(inject(function($controller, $rootScope, $location, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('RulesController', {
      $scope: this.scope,
      $location: $location,
      Rules: Rules
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching all rules", function() {
    it("should return all rules empty", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.expectGET('/api/users/superduperadmin')
      .respond(200, '{"permissions": {"admin": {"data_version": 1, "options": null}}, "roles": {}}');
      this.$httpBackend.expectGET('/api/scheduled_changes/rules')
      .respond(200, '{"scheduled_changes": [], "count": 0}');
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/required_signoffs/product')
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET('/api/emergency_shutoff')
      .respond(200, JSON.stringify({count: 0, shutoffs: []}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/scheduled_changes/emergency_shutoff')
      .respond(200, JSON.stringify({count: 0, scheduled_changes: []}));
      this.$httpBackend.flush();
      expect(this.scope.rules).toEqual([]);
    });

    it("should return all rules some", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/users/superduperadmin')
      .respond(200, '{"permissions": {"admin": {"data_version": 1, "options": null}}, "roles": {}}');
      this.$httpBackend.expectGET('/api/scheduled_changes/rules')
      .respond(200, '{"scheduled_changes": [], "count": 0}');
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/required_signoffs/product')
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET('/api/emergency_shutoff')
      .respond(200, JSON.stringify({count: 1, shutoffs: [{product: 'Firefox', channel: 'release', data_version: 1}]}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/scheduled_changes/emergency_shutoff')
      .respond(200, JSON.stringify({count: 0, scheduled_changes: []}));
      this.$httpBackend.flush();
      expect(this.scope.rules.length).toEqual(2);
      expect(this.scope.rules).toEqual(sample_rules.rules);
    });

  });

  describe("filter by select", function() {
    it("should be possible to change selected filter", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/users/superduperadmin')
      .respond(200, '{"permissions": {"admin": {"data_version": 1, "options": null}}, "roles": {}}');
      this.$httpBackend.expectGET('/api/scheduled_changes/rules')
      .respond(200, '{"scheduled_changes": [], "count": 0}');
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/required_signoffs/product')
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET('/api/emergency_shutoff')
      .respond(200, JSON.stringify({count: 1, shutoffs: [{product: 'Firefox', channel: 'release', data_version: 1}]}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/scheduled_changes/emergency_shutoff')
      .respond(200, JSON.stringify({count: 0, scheduled_changes: []}));
      this.$httpBackend.flush();

      var $scope = this.scope;
      var default_rules = $scope.pr_ch_options[0];

      expect($scope.pr_ch_filter).toEqual(default_rules);
      expect($scope.pr_ch_selected).toEqual(default_rules.split(','));
      $scope.pr_ch_filter = "foo,bar"
      $scope.$apply();
      expect($scope.pr_ch_selected).toEqual(['foo', 'bar']);
    });

  });

  describe('opening modals', function() {
    it("should be possible to open the add modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.scope.openNewRuleModal();
    });

    it("should be possible to open the edit modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.scope.openUpdateModal();
    });

    it("should be possible to open the delete modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.scope.openDeleteModal();
    });

    it("should be possible to open the revert modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.scope.openRevertModal();
    });

    it("should be possible to open the duplicate modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.scope.openDuplicateModal(sample_rules.rules[0]);
    });
  });

});


describe("controller: RulesController By Id", function() {

  beforeEach(function() {
    module("app");
  });

  var sample_revisions = {
    count: 2,
    rules: [
      {
        "buildID": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "osVersion": null,
        "instructionSet": null,
        "memory": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "fallbackMapping": null,
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "alias": null,
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor",
        "whitelist": null
      },
      {
        "buildID": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "osVersion": null,
        "instructionSet": null,
        "memory": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "fallbackMapping": null,
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "alias": null,
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor",
        "whitelist": null
      }
    ]
  };

  beforeEach(inject(function($controller, $rootScope, $location, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('RulesController', {
      $scope: this.scope,
      $location: $location,
      Rules: Rules,
      $routeParams: {id: 1}
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching specific rules", function() {

    it("should return all revisions by id", function() {
      inject(function($route, $location, $rootScope) {

        expect($route.current).toBeUndefined();
        var $scope = this.scope;
        this.$httpBackend.expectGET('/api/rules/1/revisions?limit=' + $scope.pageSize + '&page=' + $scope.currentPage)
        .respond(200, JSON.stringify(sample_revisions));

        $location.path('/rules/1');
        $rootScope.$digest();
        expect($route.current.controller).toEqual('RulesController');

        this.$httpBackend.flush();
        expect($scope.rules.length).toEqual(2);
        expect($scope.rules).toEqual(sample_revisions.rules);
      });
    });
  });

});
