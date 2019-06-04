
describe("Service: Releases", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function(Releases, $httpBackend) {
    this.$httpBackend = $httpBackend;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  it('should return all names', inject(function(Releases) {
    var sample_response = {names: ['peter', 'anders']};
    this.$httpBackend.expectGET('/api/releases?names_only=1')
    .respond(200, JSON.stringify(sample_response));
    Releases.getNames().then(function(names) {
      expect(names).toEqual(['peter', 'anders']);
    });
    this.$httpBackend.flush();
  }));

  it('should return all releases', inject(function(Releases) {
    var sample_release = {
      product: 'Firefox',
      version: '10.0',
    };
    var sample_response = {
      releases: [sample_release],
      count: 1,
    };
    this.$httpBackend.expectGET('/api/releases')
    .respond(200, JSON.stringify(sample_response));
    Releases.getReleases().success(function(response) {
      expect(response.count).toEqual(1);
      expect(response.releases[0]).toEqual(sample_release);
    });
    this.$httpBackend.flush();
  }));

  it('should return an individual release', inject(function(Releases) {
    var sample_response = {
      change_id: 123,
      product: "Firefox",
      version: "1.0",
      data_version: 3,
    };
    this.$httpBackend.expectGET('/api/releases/1')
    .respond(200, JSON.stringify(sample_response));
    Releases.getRelease(1).success(function(response) {
      expect(response).toEqual(sample_response);
    });
    this.$httpBackend.flush();
  }));

  it('should update an individual release', inject(function(Releases) {
    var sample_response = {
      new_data_version: 4,
    };
    this.$httpBackend.expectPUT('/api/releases/kitkat%202014')
    .respond(200, JSON.stringify(sample_response));
    Releases.updateRelease('kitkat 2014', {}).success(function(response) {
      expect(response).toEqual(sample_response);
    });
    this.$httpBackend.flush();
  }));

  it('should be to delete an individual release', inject(function(Releases) {
    var sample_response = {
      new_data_version: 4,
    };
    var delete_url = '/api/releases/kitkat%202014?data_version=123&csrf_token=mytoken'
    this.$httpBackend.expectDELETE(delete_url)
    .respond(200, "");
    // not that it should work if the release name has non URL safe characters
    Releases.deleteRelease('kitkat 2014', {data_version: 123}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('');
    });
    this.$httpBackend.flush();
  }));

  it('should be able to add an invidual release', inject(function(Releases) {
    this.$httpBackend.expectPOST('/api/releases')
    .respond(200, '123');
    Releases.addRelease({product: "firefox"}, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('123');
    });
    this.$httpBackend.flush();
  }));

  it('should be able to revert a release', inject(function(Releases) {
    var url = '/api/releases/kitkat%202014/revisions';
    this.$httpBackend.expectPOST(url)
    .respond(200, '');
    Releases.revertRelease('kitkat 2014', 987, 'mytoken')
    .success(function(response) {
      expect(response).toEqual('');
    });
    this.$httpBackend.flush();
  }));

});
