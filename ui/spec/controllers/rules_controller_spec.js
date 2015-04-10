describe("controller: RulesController", function() {

  beforeEach(function() {
    module("app");
  });

  var sample_rules = {
    "count": 55,
    "rules": [
      {
        "comment": "Comment",
        "product": null,
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
        "distVersion": null
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
        "distVersion": null
    }
    ]
  };

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
    it("should return all rules empty", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.flush();
      expect(this.scope.rules).toEqual([]);
    });

    it("should return all rules some", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.flush();
      expect(this.scope.rules.length).toEqual(2);
      expect(this.scope.rules).toEqual(sample_rules.rules);
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

    it("should be possible to change ordering", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.flush();

      var $scope = this.scope;
      // the default ordering should be an array based on $scope.ordering_options
      var default_ordering = $scope.ordering_options[0];

      expect($scope.ordering).toEqual(default_ordering.value.split(','));
      $scope.ordering_str = {
        'text': 'Foo then Bar',
        'value': 'foo,bar'
      }
      $scope.$apply();
      expect($scope.ordering).toEqual(['foo', 'bar']);
    });

    it("should notice if filters are on", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.flush();

      var $scope = this.scope;
      expect($scope.hasFilter()).toEqual(false);
      $scope.filters.search = 'something';
      $scope.$apply();
      expect($scope.hasFilter()).toEqual(true);
    });
  });

  describe('opening modals', function() {
    it("should be possible to open the add modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.scope.openNewRuleModal();
    });

    it("should be possible to open the edit modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.scope.openUpdateModal();
    });

    it("should be possible to open the delete modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.scope.openDeleteModal();
    });

    it("should be possible to open the revert modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.scope.openRevertModal();
    });

    it("should be possible to open the duplicate modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.scope.openDuplicateModal(sample_rules.rules[0]);
    });
  });

});


describe("controller: RulesController By Id", function() {

  beforeEach(function() {
    module("app");
  });

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
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor"
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
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor"
      }
    ]
  };

  beforeEach(inject(function($controller, $rootScope, $location, Rules, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('RulesController', {
      $scope: this.scope,
      $location: $location,
      Rules: Rules,
      $routeParams: {id: 1}
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching specific rules", function() {

    it("should return all revisions by id", function() {
      inject(function($route, $location, $rootScope) {

        expect($route.current).toBeUndefined();
        this.$httpBackend.expectGET('/api/rules/1/revisions')
        .respond(200, JSON.stringify(sample_revisions));

        $location.path('/rules/1');
        $rootScope.$digest();
        expect($route.current.controller).toEqual('RulesController');

        this.$httpBackend.flush();
        var $scope = this.scope;
        expect($scope.rules.length).toEqual(2);
        expect($scope.rules).toEqual(sample_revisions.rules);


        var default_ordering = $scope.ordering_options[0];
        expect($scope.ordering).toEqual(default_ordering.value.split(','));
        // let's be explicit, it should be hardcoded to be -data_version
        expect($scope.ordering).toEqual(['-data_version']);

      });
    });
  });

});
