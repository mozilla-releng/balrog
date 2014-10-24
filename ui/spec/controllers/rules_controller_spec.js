describe("controller: RulesController", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function($controller, $rootScope, $location, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('RulesController', {
      $scope: this.scope,
      $location: $location,
      Rules: Rules
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

  describe("filter by search", function() {
    it("should return true always if no filters active", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.flush();

      var rule_item = {
        product: "Firefox",
        channel: "nightly",
      };
      expect(this.scope.filterBySearch(rule_item)).toEqual(true);
    });

    it("should filter when only one search word name", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      $scope.filters.search = "fire";
      $scope.$apply();
      var rule_item = {
        product: "Firefox",
        channel: "nightly",
      };
      expect($scope.filterBySearch(rule_item)).toEqual(true);
      rule_item.product = "Seabird";
      expect($scope.filterBySearch(rule_item)).toEqual(false);
    });

    it("should match ALL search terms", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      $scope.filters.search = "fire night";
      $scope.$apply();
      var rule_item = {
        product: "Firefox",
        channel: "nightly",
      };
      expect($scope.filterBySearch(rule_item)).toEqual(true);
      rule_item.product = "Seabird";
      expect($scope.filterBySearch(rule_item)).toEqual(false);
      rule_item.product = "Firefox";
      rule_item.channel = "aurora"
      expect($scope.filterBySearch(rule_item)).toEqual(false);
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
