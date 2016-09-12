describe("Service: CSRF", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function(CSRF, $httpBackend) {
    this.$httpBackend = $httpBackend;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  it('should return a token', inject(function(CSRF) {
    this.$httpBackend.expectGET('/api/csrf_token')
    .respond('nothing', {'X-CSRF-Token': 'sometoken'});
    CSRF.getToken().then(function(token) {
      expect(token).toEqual('sometoken');
    });

    this.$httpBackend.expectGET('/api/csrf_token')
    .respond('nothing', {'X-CSRF-Token': 'newtoken'});
    CSRF.getToken().then(function(token) {
      // this should be the same as before because it's cached
      expect(token).toEqual('sometoken');
    });

  }));

});
