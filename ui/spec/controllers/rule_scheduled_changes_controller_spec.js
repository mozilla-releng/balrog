describe("controller: RuleScheduledChangesController", function() {
  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function($controller, $rootScope, $location, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    localStorage.setItem("username", "superduperadmin");
    // this.redirect = spyOn($location, 'path');
    $controller('RuleScheduledChangesController', {
      $scope: this.scope,
      $location: $location,
      Rules: Rules
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  var sample_user = {
    "permissions": {
      "admin": {
        "data_version": 1,
        "options": null
      },
    },
    "roles": {}
  };

  var sample_sc = {
    "count": 3,
    "scheduled_changes": [
      {
        "sc_id": 1,
        "scheduled_by": "anna",
        "when": new Date(1234),
        "complete": false,
        "telemetry_product": null,
        "telemetry_channel": null,
        "telemetry_uptake": null,
        "data_version": 1,
        "base_rule_id": 2,
        "base_priority": 50,
        "base_mapping": "thebest",
        "base_backgroundRate": 100,
        "base_update_type": "minor",
        "base_product": "Fire",
        "base_version": null,
        "base_channel": "night",
        "base_buildTarget": "win",
        "base_buildID": null,
        "base_locale": null,
        "base_osVersion": null,
        "base_instructionSet": null,
        "base_memory": null,
        "base_distribution": null,
        "base_distVersion": null,
        "base_headerArchitecture": null,
        "base_comment": null,
        "base_alias": null,
        "base_data_version": 5,
      },
      {
        "sc_id": 2,
        "scheduled_by": "joseph",
        "when": null,
        "complete": false,
        "telemetry_product": "firefox",
        "telemetry_channel": "release",
        "telemetry_uptake": 50000,
        "data_version": 2,
        "base_rule_id": null,
        "base_priority": 100,
        "base_mapping": "firefox-1000.0",
        "base_backgroundRate": 100,
        "base_update_type": "minor",
        "base_product": "Fire",
        "base_version": null,
        "base_channel": "release",
        "base_buildTarget": null,
        "base_buildID": null,
        "base_locale": null,
        "base_osVersion": null,
        "base_instructionSet": null,
        "base_memory": null,
        "base_distribution": null,
        "base_distVersion": null,
        "base_headerArchitecture": null,
        "base_comment": null,
        "base_alias": null,
        "base_data_version": null,
      },
      {
        "sc_id": 3,
        "scheduled_by": "mary",
        "when": null,
        "complete": true,
        "telemetry_product": "firefox",
        "telemetry_channel": "nightly",
        "telemetry_uptake": 500,
        "data_version": 1,
        "base_rule_id": null,
        "base_priority": 74,
        "base_mapping": "firefox-10.0",
        "base_backgroundRate": 50,
        "base_update_type": "minor",
        "base_product": "ff",
        "base_version": null,
        "base_channel": "nightly",
        "base_buildTarget": null,
        "base_buildID": null,
        "base_locale": null,
        "base_osVersion": null,
        "base_instructionSet": null,
        "base_memory": null,
        "base_distribution": null,
        "base_distVersion": null,
        "base_headerArchitecture": null,
        "base_comment": null,
        "base_alias": null,
        "base_data_version": null,
      },
    ]
  };

  describe("fetching all scheduled changes", function() {
    it("should find all scheduled changes", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();
      expect(this.scope.scheduled_changes.length).toEqual(3);
      expect(this.scope.scheduled_changes).toEqual(sample_sc.scheduled_changes);
    });
  });

  describe("filter by select", function() {
    it("should filter active scheduled changes correctly", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.state_str.value = "active";
      var $filtered = this.scope.scheduled_changes.filter(this.scope.filterBySelect);
      var $expected = this.scope.scheduled_changes.slice(0, 2);
      expect($filtered).toEqual($expected);
    });

    it("should filter completed scheduled changes correctly", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.state_str.value = "complete";
      var $filtered = this.scope.scheduled_changes.filter(this.scope.filterBySelect);
      var $expected = this.scope.scheduled_changes.slice(2, 3);
      expect($filtered).toEqual($expected);
    });
  });

  describe("opening modals", function() {
    it("should be possible to open the add modal", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.openNewScheduledRuleChangeModal();
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
    });

    it("should be possible to open the update modal for time based change", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.openUpdateModal(sample_sc.scheduled_changes[0]);
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
    });

    it("should be possible to open the update modal for telemetry change", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.openUpdateModal(sample_sc.scheduled_changes[1]);
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
    });

    it("should be possible to open the delete modal", function() {
      this.$httpBackend.expectGET("/api/users/superduperadmin")
      .respond(200, JSON.stringify(sample_user));
      this.$httpBackend.expectGET("/api/required_signoffs/product")
      .respond(200, '{"required_signoffs": [], "count": 0}');
      this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
      .respond(200, JSON.stringify(sample_sc));
      this.$httpBackend.flush();

      this.scope.openDeleteModal();
    });
  });
});
