
describe("controller: RuleEditCtrl", function() {

  beforeEach(function() {
    module("app");
  });

  var rule = {
    "comment": "Comment",
    "product": "Firefox",
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
    "whitelist": null
  };
  var pr_ch_options = ['GMP'];
  var signoffRequirements = [
    {product: "Firefox", channel: "aurora", role: "releng", signoffs_required: 2}
  ];

  beforeEach(inject(function($controller, $rootScope, $location, $modal, Rules, Releases, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');

    $controller('RuleEditCtrl', {
      $scope: this.scope,
      $modalInstance: $modal.open({
        templateUrl: 'rule_modal.html'
      }),
      $location: $location,
      Rules: Rules,
      Releases: Releases,
      rule: rule,
      pr_ch_options: pr_ch_options,
      signoffRequirements: signoffRequirements,
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the edit rule modal", function() {

    it("should set all defaults", function() {
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
      expect(this.scope.rule.product).toEqual('Firefox');
      expect(this.scope.is_edit).toEqual(true);
      expect(this.scope.ruleSignoffsRequired.length).toEqual(0);
    });

    it("should update signoff requirements when rule changes", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.flush();

      this.scope.rule.channel = 'aurora';
      this.scope.$digest();

      expect(this.scope.ruleSignoffsRequired.length).toEqual(1);
      expect(this.scope.ruleSignoffsRequired.roles['releng']).toEqual(2);
    });

    it("should be able to save changes", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      var next_data_version = rule.data_version + 1;
      this.$httpBackend.expectPUT('/api/rules/19')
      .respond(201, JSON.stringify({new_data_version: next_data_version}));

      this.scope.rule.product = 'Something';
      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();

      expect(this.scope.rule.product).toEqual('Something');
      expect(this.scope.rule.data_version).toEqual(next_data_version);
      expect(this.scope.rule.rule_id).toEqual(19);
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.errors).toEqual({});
    });

    it("should notice errors", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      var next_data_version = rule.data_version + 1;
      this.$httpBackend.expectPUT('/api/rules/19')
      .respond(400, JSON.stringify({error: 'one'}));

      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();

      expect(this.scope.errors).toEqual({error: 'one'});
      expect(this.scope.saving).toEqual(false);
    });

  });

});
