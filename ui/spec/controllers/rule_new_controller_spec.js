
describe("controller: NewRuleController", function() {

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
        "rule_id": 19,
        "priority": 1,
        "data_version": 9,
        "version": null,
        "headerArchitecture": null,
        "update_type": "minor",
        "buildTarget": null,
        "locale": null,
        "osVersion": null,
        "distribution": null,
        "channel": "nightly",
        "alias": null,
        "distVersion": null,
        "whitelist": null
    },
    {
        "comment": null,
        "product": "GMP",
        "buildID": null,
        "backgroundRate": 100,
        "mapping": "GMP-Firefox33-201410010830",
        "rule_id": 67,
        "priority": 10,
        "data_version": 2,
        "version": ">=33.0",
        "headerArchitecture": null,
        "update_type": "minor",
        "buildTarget": null,
        "locale": null,
        "osVersion": null,
        "distribution": null,
        "channel": null,
        "alias": null,
        "distVersion": null,
        "whitelist": null
    }
    ]
  };

  var sample_revisions = {
    count: 2,
    rules: [
      {
        "buildID": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "osVersion": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
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
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
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

  var rules = sample_rules.rules;
  var rule = {
    product: '',
    backgroundRate: 0,
    priority: 0,
    update_type: 'minor',
    _duplicate: false,
  };

  beforeEach(inject(function($controller, $rootScope, $location, $modal, Rules, Releases, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');

    $controller('NewRuleCtrl', {
      $scope: this.scope,
      $modalInstance: $modal.open({
        templateUrl: 'rule_modal.html'
      }),
      $location: $location,
      Rules: Rules,
      Releases: Releases,
      rules: rules,
      rule: rule,
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the new rule modal", function() {

    it("should should all defaults", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.flush();
      expect(this.scope.names).toEqual(['Name1', 'Name2']);
      expect(this.scope.channels).toEqual(['Channel1', 'Channel2']);
      expect(this.scope.products).toEqual(['Product1', 'Product2']);
      expect(this.scope.errors).toEqual({});
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.rule).toEqual(rule);
      expect(this.scope.rule.product).toEqual('');
      expect(this.scope.rules).toEqual(rules);
      expect(this.scope.is_edit).toEqual(false);
      expect(this.scope.is_duplicate).toEqual(false);
    });

    it("should should be able to save changes", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPOST('/api/rules')
      .respond(201, '123');

      this.scope.rule.product = 'Something';
      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();

      expect(this.scope.rule.data_version).toEqual(1);
      expect(this.scope.rule.rule_id).toEqual(123);
      expect(this.scope.rules.length).toEqual(3);
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.errors).toEqual({});
    });

    it("should should throw sweetAlert on error", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      this.$httpBackend.expectPOST('/api/rules')
      .respond(400, '{"error": "one"}');

      this.scope.rule.product = 'Something';
      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();

      expect(this.scope.errors).toEqual({error: 'one'});
      expect(this.scope.saving).toEqual(false);
    });

  });

});
