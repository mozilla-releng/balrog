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
        "systemCapabilities": null,
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
        "systemCapabilities": null,
        "distribution": null,
        "channel": null,
        "alias": null,
        "distVersion": null,
        "whitelist": null
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
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.flush();
      expect(this.scope.rules).toEqual([]);
    });

    it("should return all rules some", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.flush();
      expect(this.scope.rules.length).toEqual(2);
      expect(this.scope.rules).toEqual(sample_rules.rules);
    });

  });

  describe("filter by select", function() {
    it("should be possible to change selected filter", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.flush();

      var $scope = this.scope;
      // the default ordering should be an array based on $scope.ordering_options
      var default_rules = $scope.pr_ch_options[0];

      expect($scope.pr_ch_filter).toEqual(default_rules);
      expect($scope.pr_ch_selected).toEqual(default_rules.split(','));
      $scope.pr_ch_filter = "foo,bar"
      $scope.$apply();
      expect($scope.pr_ch_selected).toEqual(['foo', 'bar']);
    });

    it("should be possible to change ordering", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
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
  });

  describe('opening modals', function() {
    it("should be possible to open the add modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      this.scope.openNewRuleModal();
    });

    it("should be possible to open the edit modal", function() {
      this.$httpBackend.expectGET('/api/rules')
      .respond(200, JSON.stringify(sample_rules));
      this.$httpBackend.expectGET('/api/releases?names_only=1')
      .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
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
      this.$httpBackend.expectGET('/api/rules/columns/channel')
      .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
      this.$httpBackend.expectGET('/api/rules/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
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
        "systemCapabilities": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "alias": null,
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor",
        "whitelist": null
      },
      {
        "buildID": null,
        "comment": "Comment",
        "product": null,
        "change_id": 59,
        "osVersion": null,
        "systemCapabilities": null,
        "locale": null,
        "timestamp": 1384364357223,
        "changed_by": "bhearsum@mozilla.com",
        "mapping": "No-Update",
        "priority": 1,
        "data_version": 1,
        "version": null,
        "background_rate": 100,
        "alias": null,
        "distVersion": null,
        "headerArchitecture": null,
        "distribution": null,
        "buildTarget": null,
        "id": 19,
        "channel": null,
        "update_type": "minor",
        "whitelist": null
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
        var $scope = this.scope;
        this.$httpBackend.expectGET('/api/rules/1/revisions?limit=' + $scope.pageSize + '&page=' + $scope.currentPage)
        .respond(200, JSON.stringify(sample_revisions));

        $location.path('/rules/1');
        $rootScope.$digest();
        expect($route.current.controller).toEqual('RulesController');

        this.$httpBackend.flush();
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
