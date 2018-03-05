describe("Service: EmergencyShutoffs", function() {
  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function($httpBackend) {
    this.$httpBackend = $httpBackend;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  it("should return all shutoffs even empty", inject(function(EmergencyShutoffs) {
    var sample_response = {count: 0, shutoffs: []};
    this.$httpBackend.expectGET('/api/emergency_shutoff')
    .respond(200, JSON.stringify(sample_response));
    EmergencyShutoffs.get().success(function(response) {
      expect(response.count).toEqual(0);
      expect(response.shutoffs).toEqual([]);
    });
    this.$httpBackend.flush();
  }));

  it("should return all shutoffs with something", inject(function(EmergencyShutoffs) {
    var sample_shutoff = {product: 'Fennec', channel: 'beta', data_version:1};
    var sample_response = {count: 1, shutoffs: [sample_shutoff]};
    this.$httpBackend.expectGET('/api/emergency_shutoff')
    .respond(200, JSON.stringify(sample_response));
    EmergencyShutoffs.get().success(function(response) {
      expect(response.count).toEqual(1);
      expect(response.shutoffs[0]).toEqual(sample_shutoff);
    });
    this.$httpBackend.flush();
  }));

  it("should disable updates", inject(function(EmergencyShutoffs) {
    var sample_shutoff = {product: 'Fennec', channel: 'beta', data_version:1};
    this.$httpBackend.expectPOST('/api/emergency_shutoff')
    .respond(200, JSON.stringify(sample_shutoff));
    EmergencyShutoffs.create('Fennec', 'beta').success(function(response) {
      expect(response).toEqual(sample_shutoff);
    });
    this.$httpBackend.flush();
  }));

  it("should enable updates", inject(function(EmergencyShutoffs) {
    var deleteUrl = '/api/emergency_shutoff/Firefox/release?data_version=1&csrf_token=mtk';
    this.$httpBackend.expectDELETE(deleteUrl).respond(200);
    EmergencyShutoffs.delete('Firefox', 'release', 1, 'mtk');
    this.$httpBackend.flush();
  }));

  it("should return all scheduled changes even empty", inject(function(EmergencyShutoffs) {
    var sample_response = {count: 0, scheduled_changes: []};
    this.$httpBackend.expectGET('/api/scheduled_changes/emergency_shutoff')
    .respond(200, JSON.stringify(sample_response));
    EmergencyShutoffs.scheduledChanges().success(function(response) {
      expect(response.count).toEqual(0);
      expect(response.scheduled_changes).toEqual([]);
    });
    this.$httpBackend.flush();
  }));

  it("should return all scheduled changes with something", inject(function(EmergencyShutoffs) {
    var scheduled_change = {
      change_type: "delete",
      channel: "release",
      complete: false,
      data_version: 1,
      original_row: {
        channel: "release",
        data_version: 1,
        product: "Firefox"
      },
      product: "Firefox",
      required_signoffs: {
        releng: 1
      },
      sc_data_version: 1,
      sc_id: 80,
      scheduled_by: "balrogadmin",
      signoffs: {},
      when: 1518357656007
    };

    var sample_response = {count: 1, scheduled_changes: [scheduled_change]};

    this.$httpBackend.expectGET('/api/scheduled_changes/emergency_shutoff')
    .respond(200, JSON.stringify(sample_response));

    EmergencyShutoffs.scheduledChanges().success(function(response) {
      expect(response.count).toEqual(1);
      expect(response.scheduled_changes[0]).toEqual(scheduled_change);
    });
    this.$httpBackend.flush();
  }));

  it("should schedule to enable updates", inject(function(EmergencyShutoffs) {
    var sample_response = {sc_id: 1};
    this.$httpBackend.expectPOST('/api/scheduled_changes/emergency_shutoff')
    .respond(200, JSON.stringify(sample_response));
    EmergencyShutoffs.scheduleEnableUpdates({},'mtk').success(function(response) {
      expect(response).toEqual(sample_response);
    });
    this.$httpBackend.flush();
  }));

  it("should keep updates disabled", inject(function(EmergencyShutoffs) {
    var deleteUrl = '/api/scheduled_changes/emergency_shutoff/1?data_version=1&csrf_token=mtk';
    this.$httpBackend.expectDELETE(deleteUrl).respond(200);
    EmergencyShutoffs.deleteScheduledEnableUpdates(1, 1, 'mtk');
    this.$httpBackend.flush();
  }));

  it("should return scheduled change for shutoff", inject(function(EmergencyShutoffs) {
    var scheduled_change = {
      change_type: "delete",
      channel: "release",
      complete: false,
      data_version: 1,
      original_row: {
        channel: "release",
        data_version: 1,
        product: "Firefox"
      },
      product: "Firefox",
      required_signoffs: {
        releng: 1
      },
      sc_data_version: 1,
      sc_id: 80,
      scheduled_by: "balrogadmin",
      signoffs: {},
      when: 1518357656007
    };
    var scheduled_changes = [scheduled_change];
    var shutoff = {product: 'Firefox', channel: 'release'};
    var sc = EmergencyShutoffs.shutoffScheduledEnableChange(shutoff, scheduled_changes);
    expect(sc).toEqual(scheduled_change);
  }));

  it("should return null scheduled change for shutoff", inject(function(EmergencyShutoffs) {
    var scheduled_change = {
      change_type: "delete",
      channel: "release",
      complete: false,
      data_version: 1,
      original_row: {
        channel: "release",
        data_version: 1,
        product: "Firefox"
      },
      product: "Firefox",
      required_signoffs: {
        releng: 1
      },
      sc_data_version: 1,
      sc_id: 80,
      scheduled_by: "balrogadmin",
      signoffs: {},
      when: 1518357656007
    };
    var scheduled_changes = [scheduled_change];
    var shutoff = {product: 'Firefox', channel: 'beta'};
    var sc = EmergencyShutoffs.shutoffScheduledEnableChange(shutoff, scheduled_changes);
    expect(sc).toEqual(null);
  }));
});