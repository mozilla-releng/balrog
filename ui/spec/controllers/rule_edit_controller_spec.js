
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
  };

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
