
describe("controller: RuleEditCtrl", function() {

  beforeEach(function() {
    module("app");
  });

  var sample_rules = {
    "count": 55,
    "rules": [
      {
        "comment": "Comment",
        "product": "Firefox",
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
        "distVersion": null
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
        "distVersion": null
    }
    ]
  };

  var XXXXsample_revisions = {
    count: 2,
    rules: [
      {
        "build_id": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "os_version": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "dist_version": null,
        "header_arch": null,
        "distribution": null,
        "build_target": null,
        "id": 19,
        "channel": null,
        "update_type": "minor"
      },
      {
        "build_id": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "os_version": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "dist_version": null,
        "header_arch": null,
        "distribution": null,
        "build_target": null,
        "id": 19,
        "channel": null,
        "update_type": "minor"
      }
    ]
  };

  var rules = sample_rules.rules;
  var rule = rules[0];

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
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the edit rule modal", function() {

    it("should should all defaults", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.flush();
      expect(this.scope.names).toEqual(['Name1', 'Name2']);
      expect(this.scope.errors).toEqual({});
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.rule).toEqual(rule);
      expect(this.scope.rule.product).toEqual('Firefox');
      expect(this.scope.is_edit).toEqual(true);
    });

    it("should should be able to save changes", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
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

    it("should should notice errors", function() {
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
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
