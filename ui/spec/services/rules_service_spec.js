describe("Service: Rules", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function(Rules, $httpBackend) {
    this.$httpBackend = $httpBackend;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  it('should return all rules even empty', inject(function(Rules) {
    var sample_response = {rules: [], count: 0};
    this.$httpBackend.expectGET('/api/rules')
    .respond(200, JSON.stringify(sample_response));
    Rules.getRules().success(function(response) {
      expect(response.count).toEqual(0);
      expect(response.rules).toEqual([]);
    });
    this.$httpBackend.flush();
  }));

  it('should return all rules with something', inject(function(Rules) {
    var sample_rule = {
      product: 'Firefox'
    };
    var sample_response = {
      rules: [sample_rule],
      count: 1,
    };
    this.$httpBackend.expectGET('/api/rules')
    .respond(200, JSON.stringify(sample_response));
    Rules.getRules().success(function(response) {
      expect(response.count).toEqual(1);
      expect(response.rules[0]).toEqual(sample_rule);
    });
    this.$httpBackend.flush();
  }));

  it('should return all rules history', inject(function(Rules) {
    var sample_response = {
      rules: [{
        change_id: 123,
        product: "Firefox",
        data_version: 3,
      }, {
        change_id: 122,
        product: "Firefoxy",
        data_version: 2,
      }],
      count: 2
    };
    var limit = 10;
    var page = 1;
    this.$httpBackend.expectGET('/api/rules/1/revisions?limit=' + limit + '&page=' + page)
    .respond(200, JSON.stringify(sample_response));
    Rules.getHistory(1, limit, page).success(function(response) {
      expect(response.count).toEqual(2);
      expect(response.rules).toEqual(sample_response.rules);
    });
    this.$httpBackend.flush();
  }));

  it('should return an individual rule', inject(function(Rules) {
    var sample_response = {
      change_id: 123,
      product: "Firefox",
      data_version: 3,
    };
    this.$httpBackend.expectGET('/api/rules/1')
    .respond(200, JSON.stringify(sample_response));
    Rules.getRule(1).success(function(response) {
      expect(response).toEqual(sample_response);
    });
    this.$httpBackend.flush();
  }));

  it('should update an individual rule', inject(function(Rules) {
    var sample_response = {
      new_data_version: 4,
    };
    this.$httpBackend.expectPUT('/api/rules/1')
    .respond(200, JSON.stringify(sample_response));
    Rules.updateRule(1, {}).success(function(response) {
      expect(response).toEqual(sample_response);
    });
    this.$httpBackend.flush();
  }));

  it('should be to delete an individual rule', inject(function(Rules) {
    var sample_response = {
      new_data_version: 4,
    };
    var delete_url = '/api/rules/1?data_version=123&csrf_token=mytoken'
    this.$httpBackend.expectDELETE(delete_url)
    .respond(200, '');
    Rules.deleteRule(1, {data_version: 123}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('');
    });
    this.$httpBackend.flush();
  }));

  it('should be able to add an invidual rule', inject(function(Rules) {
    this.$httpBackend.expectPOST('/api/rules')
    .respond(200, '123');
    Rules.addRule({product: "firefox"}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('123');
    });
    this.$httpBackend.flush();
  }));

  it('should be able to add an revert a rule', inject(function(Rules) {
    var url = '/api/rules/123/revisions';
    this.$httpBackend.expectPOST(url)
    .respond(200, '');
    Rules.revertRule(123, 987, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('');
    });
    this.$httpBackend.flush();
  }));

  it("should return all scheduled rule changes", inject(function(Rules) {
    var sample_sc = {
      "sc_id": 1,
      "scheduled_by": "jess",
      "complete": false,
      "when": new Date(123456789),
      "base_rule_id": 2,
      "base_product": "Firefox",
      "base_channel": "release",
      "base_data_version": 1
    };
    var sample_response = {
      count: 1,
      scheduled_changes: [sample_sc]
    };
    this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
    .respond(200, JSON.stringify(sample_response));
    Rules.getScheduledChanges().success(function(response) {
      expect(response.count).toEqual(1);
      expect(response.scheduled_changes[0]).toEqual(sample_sc);
    });
  }));

  it("should return a single scheduled rule change", inject(function(Rules) {
    var sample_response = {
      "sc_id": 1,
      "scheduled_by": "jess",
      "complete": false,
      "when": new Date(123456789),
      "base_rule_id": 2,
      "base_product": "Firefox",
      "base_channel": "release",
      "base_data_version": 1
    };
    this.$httpBackend.expectGET("/api/scheduled_changes/rules/1")
    .respond(200, JSON.stringify(sample_response));
    Rules.getScheduledChange(1).success(function(response) {
      expect(response).toEqual(sample_response);
    });
  }));

  it("should be able to create a scheduled change", inject(function(Rules) {
    var sample_response = {
      sc_id: 1
    };
    this.$httpBackend.expectPOST("/api/scheduled_changes/rules")
    .respond(200, JSON.stringify(sample_response));
    Rules.addScheduledChange({"when": new Date(123456789), "base_product": "Foo"}, "csrf").success(function(response) {
      expect(response.sc_id).toEqual(1);
    });
  }));

  it("should be able to update a scheduled change", inject(function(Rules) {
    var sample_response = {
      new_data_version: 2
    };
    this.$httpBackend.expectPOST("/api/scheduled_changes/rules/2")
    .respond(200, JSON.stringify(sample_response));
    Rules.updateScheduledChange(2, {"when": new Date(123456789), "base_mapping": "abc", "data_version": 1}, "csrf")
    .success(function(response) {
      expect(response).toEqual(sample_response);
    });
  }));

  it("should be able to delete a scheduled change", inject(function(Rules) {
    this.$httpBackend.expectDELETE("/api/scheduled_changes/rules/3?data_version=2&csrf_token=csrf")
    .respond(200);
    Rules.deleteScheduledChange(3, {sc_data_version: 2}, "csrf");
  }));

  // todo: add sc history methods
});
