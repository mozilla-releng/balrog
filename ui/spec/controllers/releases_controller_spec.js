var sample_revisions = {
  "count": 2,
  "revisions": [
    {
      "product": "Firefox",
      "name": "Firefox-33.0-build1",
      "data_url": "fake",
      "change_id": 713662,
      "changed_by": "ffxbld",
      "data_version": 1,
      "version": "33.0",
      "_different": [],
      "timestamp": 1412700789587,
      "_time_ago": "1 month and 6 weeks ago",
      "data": "{\"hashFunction\": \"sha512\", \"name\": \"Firefox-33.0-build1\", \"schema_version\": 3}"
    },
    {
      "product": "Firefox",
      "name": "Firefox-33.0-build1",
      "data_url": "fake",
      "change_id": 713663,
      "changed_by": "ffxbld",
      "data_version": 2,
      "version": "33.0",
      "_different": [
        "data"
      ],
      "timestamp": 1412700789642,
      "_time_ago": "1 month and 6 weeks ago",
      "data": "{\"platforms\": {\"Darwin_x86_64-gcc3-u-i386-x86_64\": {\"locales\": {\"en-US\": {\"buildID\": \"20141007073543\"}",
    }]
  };

var sample_releases = {
  "releases": [
    {
      "data_version": 2,
      "product": "B2G",
      "version": "34.0a2",
      "name": "B2G-mozilla-aurora-kitkat-nightly-20140923151000",
      "data_link": "fake",
      "required_signoffs": {},
    },
    {
      "data_version": 2,
      "product": "B2G",
      "version": "34.0a2",
      "name": "B2G-mozilla-aurora-kitkat-nightly-20140923160203",
      "data_link": "fake",
      "required_signoffs": {},
    },
    {
      "data_version": 4,
      "product": "Fennec",
      "version": "30.0a2",
      "name": "Fennec-mozilla-aurora-nightly-20140410004003",
      "data_link": "fake",
      "required_signoffs": {},
    }
  ],
  "count": 3
};

var release = sample_releases.releases[0];

describe("controller: ReleasesController", function() {

  beforeEach(function() {
    module("app");
  });

  beforeEach(inject(function($controller, $rootScope, $location, Releases, $httpBackend) {
    this.$location = $location;
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    // this.redirect = spyOn($location, 'path');
    $controller('ReleasesController', {
      $scope: this.scope,
      $location: $location,
      Releases: Releases
    });
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching releases", function() {
    it("should return all releases empty", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, '{"releases": [], "count": 0}');
      this.$httpBackend.flush();
      expect(this.scope.releases).toEqual([]);
    });

    it("should return all releases", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();
      expect(this.scope.releases.length).toEqual(3);
      var transformedReleases = angular.copy(sample_releases.releases);
      transformedReleases.forEach(function(release) {
        release.required_signoffs = {length: 0, roles: {}};
      });
      expect(this.scope.releases).toEqual(transformedReleases);
    });

  });

  describe("filter by search", function() {
    it("should return true always if no filters active", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, '{"releases": [], "count": 0}');
      this.$httpBackend.flush();

      var item = {
        product: "Firefox",
        version: "35",
        name: "Firefox-35-build1"
      };
      expect(this.scope.filterBySearch(item)).toEqual(true);
    });

    it("should filter when only one search word name", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, '{"releases": [], "count": 0}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      $scope.filters.search = "fire";
      $scope.$apply();
      var item = {
        product: "Firefox",
        version: "35",
        name: "Firefox-35-build1"
      };
      expect($scope.filterBySearch(item)).toEqual(true);
      item.product = "Seabird";
      item.name = "Seabird-11-buildX";
      expect($scope.filterBySearch(item)).toEqual(false);
    });

    it("should match ALL search terms", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, '{"releases": [], "count": 0}');
      this.$httpBackend.flush();

      var $scope = this.scope;
      $scope.filters.search = "fire build";
      $scope.$apply();
      var item = {
        product: "Firefox",
        version: "35",
        name: "Firefox-35-build1"
      };
      // matches both on "fire" and on "build"
      expect($scope.filterBySearch(item)).toEqual(true);
      item.product = "Seabird";
      // matches on "fire" and "build" still, both for 'name'
      expect($scope.filterBySearch(item)).toEqual(true);
      item.name = 'fennec-10-build';
      // now "build" matches but "fire" doesn't
      expect($scope.filterBySearch(item)).toEqual(false);
    });

    it("should be possible to change ordering", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
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
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
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
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();
      // this.$httpBackend.expectGET('/api/releases?names_only=1')
      // .respond(200, JSON.stringify({names: ['Name1', 'Name2']}));
      this.scope.openNewReleaseModal();
      this.$httpBackend.expectGET('/api/releases/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
      // this.$httpBackend.flush();
      // this.$httpBackend.verifyNoOutstandingRequest();
      // this.$httpBackend.verifyNoOutstandingExpectation();
    });
    //
    it("should be possible to open the edit modal", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();
      this.scope.openUpdateModal(sample_releases.releases[0]);
      this.$httpBackend.expectGET('/api/releases/columns/product')
      .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
    });

    it("should be possible to open the delete modal", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();
      this.scope.openDeleteModal(sample_releases.releases[0]);
    });

    it("should be possible to open the data modal", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();

      this.$httpBackend.expectGET('/api/releases/' + release.name)
      .respond(200, JSON.stringify(sample_releases));
      this.scope.openDataModal(release);
      this.$httpBackend.flush();
    });

    it("should be possible to open the diff modal", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.flush();

      this.$httpBackend.expectGET('/api/releases/' + release.name)
      .respond(200, JSON.stringify(sample_releases));
      this.scope.openDiffModal(release);
      this.$httpBackend.flush();
    });

    it("should be possible to open the revert modal", function() {
      this.$httpBackend.expectGET('/api/releases')
      .respond(200, JSON.stringify(sample_releases));
      this.$httpBackend.expectGET('fake')
      .respond(200, "fake");
      this.scope.openRevertModal(sample_revisions.revisions[0]);
    });
  });

});
