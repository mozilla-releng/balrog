
describe("controller: RuleDeleteCtrl", function() {

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

  var rules = sample_rules.rules;
  var rule = rules[0];

  beforeEach(inject(function($controller, $rootScope, $location, $modal, CSRF, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');

    $controller('RuleDeleteCtrl', {
      $scope: this.scope,
      $modalInstance: $modal.open({
        templateUrl: 'rule_delete_modal.html'
      }),
      CSRF: CSRF,
      Rules: Rules,
      rules: rules,
      rule: rule,
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("opening the delete rule modal", function() {

    it("should say something about the rule", function() {
      expect(this.scope.saving).toEqual(false);
      expect(this.scope.rule).toEqual(rule);
      expect(this.scope.rules).toEqual(rules);
      expect(this.scope.rule.product).toEqual('Firefox');

      // click the cancel button should work
      this.scope.cancel();

    });

    it("should be possible to delete the rule", function() {
      this.$httpBackend.expectGET('/api/csrf_token')
      .respond('nothing', {'X-CSRF-Token': 'sometoken'});
      expect(this.scope.saving).toEqual(false);
      this.$httpBackend.expectDELETE(
        '/api/rules/19?data_version=' + rule.data_version + '&csrf_token=sometoken'
      )
      .respond(200, '');

      this.scope.saveChanges();
      expect(this.scope.saving).toEqual(true);
      this.$httpBackend.flush();
      expect(this.scope.saving).toEqual(false);

    });

  });

});
