describe("controller: RulesController", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function($controller, $rootScope, $location, RulesService, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('RulesController', {
      $scope: this.scope,
      $location: $location,
      RulesService: RulesService
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching all rules", function() {
    it("should return all rules", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.flush();
      // console.log('scope', this.scope.total_count)
      expect(this.scope.total_count).toEqual(0);
      expect(this.scope.rules).toEqual([]);
    });

  });
  // describe("successfully logging in", function() {
  //   it("should redirect you to /home", function() {
  //     this.$httpBackend.expectPOST('/login', this.scope.credentials).respond(200);
  //     this.scope.login();
  //     this.$httpBackend.flush();
  //     expect(this.redirect).toHaveBeenCalledWith('/home');
  //   });
  // });
});
