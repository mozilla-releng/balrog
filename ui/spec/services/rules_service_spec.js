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
    this.$httpBackend.expectGET('/api/rules/1/revisions')
    .respond(200, JSON.stringify(sample_response));
    Rules.getHistory(1).success(function(response) {
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

  it('should be set aliases on a rule', inject(function(Rules) {
    var rule = {
      buildID: '123',
      buildTarget: '456',
      osVersion: '789',
      distVersion: 111,
      headerArchitecture: 222
    };
    Rules.setDataAliases(rule);
    expect(rule.build_id).toEqual('123');
    expect(rule.build_target).toEqual('456');
    expect(rule.os_version).toEqual('789');
    expect(rule.dist_version).toEqual(111);
    expect(rule.header_arch).toEqual(222);
  }));



});
