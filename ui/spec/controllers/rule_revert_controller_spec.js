
describe("controller: RuleRevertCtrl", function() {

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
    "alias": null,
    "distVersion": null,
    "whitelist": null
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

  var revision = sample_revisions.rules[0];

  beforeEach(inject(function($controller, $rootScope, $location, $modal, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');

    $controller('RuleRevertCtrl', {
      $scope: this.scope,
      $modalInstance: $modal.open({
        templateUrl: 'rule_revert_modal.html'
      }),
      $location: $location,
      Rules: Rules,
      revision: revision,
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the revert rule modal", function() {

    it("should should set all defaults", function() {
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.rule).toEqual(revision);
      expect(this.scope.rule.comment).toEqual('Comment');
    });

    it("should should be able to save changes", function() {
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond(200, 'token');
      var next_data_version = rule.data_version + 1;
      this.$httpBackend.expectPOST('/api/rules/19/revisions')
      .respond(200, 'ok');

      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();

    });
  });

});
