describe("controller: HistoryController", function() {
  beforeEach(function() {
    module("app");
  });
  var changed_by_response = {
    changed_by: "hope.ngerebara@gmail.com",
    channel: "release-cdntest"
  };
  var sample_rules_response = {
    Rules: {
      count: 2,
      revisions: [
        {
          alias: null,
          change_id: 9490,
          changed_by: "hope.ngerebara@gmail.com",
          channel: "release-cdntest",
          data_version: 3,
          product: "Firefox",
          rule_id: 665,
          timestamp: 1508923005724,
          type: "Rules"
        },
        {
          alias: null,
          change_id: 9489,
          changed_by: "hope.ngerebara@gmail.com",
          channel: "release-cdntest",
          data_version: 2,
          product: "Firefox",
          rule_id: 666,
          timestamp: 1508923005671,
          type: "Rules"
        }
      ]
    },
    "Rules scheduled change": {
      count: 1,
      revisions: [
        {
          alias: null,
          change_id: 2,
          change_type: "update",
          changed_by: "hope.ngerebara@gmail.com",
          channel: "nightlytest",
          product: "Thunderbird",
          rule_id: 633,
          sc_id: 1,
          scheduled_by: "balrogadmin",
          timestamp: 1509379903963,
          when: 1510700400000,
          type: "Rules scheduled change"
        }
      ]
    }
  };

  var sample_releases_response = {
    Releases: {
      count: 3,
      revisions: [
        {
          _different: [],
          _time_ago: "1 day ago",
          change_id: 12635504,
          changed_by: "hope.ngerebara@gmail.com",
          data_version: 798882,
          name: "Firefox-mozilla-central-nightly-latest",
          product: "Firefox",
          read_only: "False",
          timestamp: 1508923005671,
          type: "Releases"
        },
        {
          _different: ["name", "data"],
          _time_ago: "13 days ago",
          change_id: 12598208,
          changed_by: "hope.ngerebara@gmail.com",
          data_version: 1100,
          name: "Firefox-56.0.2-build1",
          product: "Firefox",
          read_only: "False",
          timestamp: 1508923005671,
          type: "Releases"
        }
      ]
    },
    "Releases scheduled change": {
      count: 0,
      revisions: []
    }
  };

  var sample_permissions_response = {
    Permissions: {
      count: 2,
      revisions: [
        {
          change_id: 20,
          changed_by: "hope.ngerebara@gmail.com",
          data_version: 1,
          options: null,
          permission: "release_locale",
          timestamp: 1510747027498,
          username: "Hope",
          type: "Permissions"
        },
        {
          change_id: 19,
          changed_by: "hope.ngerebara@gmail.com",
          data_version: null,
          options: null,
          permission: "admin",
          timestamp: 1510747027497,
          username: "Colins",
          type: "Permissions"
        }
      ]
    }
  };
  var $scope;
  beforeEach(
    inject(function($controller, $rootScope, History, $httpBackend) {
      this.$httpBackend = $httpBackend;
      this.scope = $rootScope.$new();
      $controller("HistoryController", {
        $scope: this.scope,
        History: History
      });
    })
  );

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching all History", function() {
    it("should return an empty search result", function() {
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend
        .expectGET("/api/rules/columns/product")
        .respond(
          200,
          JSON.stringify({ product: ["Product1", "Product2"], count: 2 })
        );
      this.$httpBackend
        .expectGET("/api/rules/columns/channel")
        .respond(
          200,
          JSON.stringify({ channel: ["Channel1", "Channel2"], count: 2 })
        );
      this.$httpBackend.flush();
      expect(this.scope.searchResult).toEqual([]);
    });
  });

  describe("Filters", function() {
    it("should return the response when 'rules' object is selected", function() {
      this.scope.data.objectSelected = {
        id: "2",
        name: "all_rules",
        value: "Rules"
      };
      this.scope.searchHistory();
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, '{"rules": [], "count": 0}');
      this.$httpBackend.expectGET("/api/all_rules/history?&page=1")
        .respond(200,
          JSON.stringify({
            Rules: { count: 2, revisions: ["test2", "test"] },
            "Rules Scheduled Change": { count: 1, revisions: [] }
          })
        );
      this.$httpBackend
        .expectGET("/api/rules/columns/product")
        .respond(200,JSON.stringify({ product: ["Product1", "Product2"], count: 2 }));
      this.$httpBackend
        .expectGET("/api/rules/columns/channel")
        .respond(200,JSON.stringify({ channel: ["Channel1", "Channel2"], count: 2 }));
      this.$httpBackend.flush();
      expect(this.scope.searchResult).toEqual(["test", "test2"]);
    });

    it("should return the data when the changed_by name is entered", function() {
      this.scope.data.objectSelected = {
        id: "2",
        name: "all_rules",
        value: "Rules"
      };
      this.scope.userInput = {
        changedBy: "hope.ngerebara@gmail.com",
        dateRangeStart: 1508923005671,
        dateRangeEnd: 1508923005724
      };
      this.scope.searchHistory();
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, '{"rules": [], "count": 0}');
      var result = [];
      var index = 0;
      angular.forEach(sample_rules_response, function(value, key) {
        result.push(value.revisions);
      });
      this.$httpBackend
        .expectGET(
          "/api/all_rules/history?&page=1&changed_by=hope.ngerebara@gmail.com&timestamp_from=1508923005671&timestamp_to=1508923005724"
        )
        .respond(200, JSON.stringify(sample_rules_response));
      this.$httpBackend
        .expectGET("/api/rules/columns/product")
        .respond(
          200,
          JSON.stringify({ product: ["Product1", "Product2"], count: 2 })
        );
      this.$httpBackend
        .expectGET("/api/rules/columns/channel")
        .respond(
          200,
          JSON.stringify({ channel: ["Channel1", "Channel2"], count: 2 })
        );
      this.$httpBackend.flush();
      expect(this.scope.searchResult[1]).toEqual(result[0][0]);
    });

    it("should return data when 'release' object is selected", function() {
      this.scope.data.objectSelected = {
        id: "3",
        name: "all_releases",
        value: "Releases"
      };
      this.scope.userInput = {
        changedBy: "hope.ngerebara@gmail.com",
        dateRangeStart: 1508923005671,
        dateRangeEnd: 1508923005724
      };
      this.scope.searchHistory();
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, '{"rules": [], "count": 0}');
      var result = [];
      angular.forEach(sample_releases_response, function(value, key) {
        result.push(value.revisions);
      });
      this.$httpBackend
        .expectGET(
          "/api/all_releases/history?&page=1&changed_by=hope.ngerebara@gmail.com&timestamp_from=1508923005671&timestamp_to=1508923005724"
        )
        .respond(200, JSON.stringify(sample_releases_response));
      this.$httpBackend
        .expectGET("/api/rules/columns/product")
        .respond(
          200,
          JSON.stringify({ product: ["Product1", "Product2"], count: 2 })
        );
      this.$httpBackend
        .expectGET("/api/rules/columns/channel")
        .respond(
          200,
          JSON.stringify({ channel: ["Channel1", "Channel2"], count: 2 })
        );
      this.$httpBackend.flush();
      expect(this.scope.searchResult[1]).toEqual(result[0][0]);
    });

    it("should return data when 'permissions' object is selected", function() {
      this.scope.data.objectSelected = {
        id: "4",
        name: "all_permissions",
        value: "Permissions"
      };
      this.scope.userInput = {
        changedBy: "hope.ngerebara@gmail.com",
        dateRangeStart: 1510747027497,
        dateRangeEnd: 1510747027498
      };
      this.scope.searchHistory();
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, '{"rules": [], "count": 0}');
      var result = [];
      angular.forEach(sample_permissions_response, function(value, key) {
        result.push(value.revisions);
      });
      this.$httpBackend
        .expectGET(
          "/api/all_permissions/history?&page=1&changed_by=hope.ngerebara@gmail.com&timestamp_from=1510747027497&timestamp_to=1510747027498"
        )
        .respond(200, JSON.stringify(sample_permissions_response));
      this.$httpBackend
        .expectGET("/api/rules/columns/product")
        .respond(
          200,
          JSON.stringify({ product: ["Product1", "Product2"], count: 2 })
        );
      this.$httpBackend
        .expectGET("/api/rules/columns/channel")
        .respond(
          200,
          JSON.stringify({ channel: ["Channel1", "Channel2"], count: 2 })
        );
      this.$httpBackend.flush();
      expect(this.scope.searchResult).toEqual(result[0]);
    });
  });
});
