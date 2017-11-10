describe("Service: History", function() {
  beforeEach(function() {
    module("app");
  });

  beforeEach(
    inject(function(History, $httpBackend) {
      this.$httpBackend = $httpBackend;
    })
  );

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  var sample_rules_response = {
    Rules: {
      count: 2,
      revisions: [
        {
          alias: null,
          backgroundRate: 100,
          buildID: null,
          buildTarget: "WINNT_x86-msvc-x64",
          change_id: 9490,
          changed_by: "hope.ngerebara@gmail.com",
          channel: "release-cdntest",
          comment: "Watershed",
          priority: 94,
          product: "Firefox",
          rule_id: 665,
          timestamp: 1508923005724,
          update_type: "minor",
          version: "<56.0.1"
        },
        {
          alias: null,
          backgroundRate: 100,
          buildID: null,
          buildTarget: "WINNT_x86-msvc-x64",
          change_id: 9499,
          changed_by: "hope.ngerebara@gmail.com",
          channel: "release-cdntest",
          comment: "Watershed 2",
          priority: 94,
          product: "Firefox",
          rule_id: 666,
          timestamp: 1508923005755,
          update_type: "minor",
          version: "<56.0.1"
        }
      ]
    },
    "Rules scheduled change": {
      count: 1,
      revisions: [
        {
          alias: null,
          backgroundRate: 0,
          buildID: ">=20170730030209",
          buildTarget: null,
          change_id: 2,
          change_type: "update",
          changed_by: "hopez",
          channel: "nightlytest",
          mapping: "Thunderbird-comm-central-nightly-latest",
          product: "Thunderbird",
          rule_id: 633,
          sc_data_version: 1,
          sc_id: 1,
          scheduled_by: "balrogadmin",
          timestamp: 1509379903963,
          update_type: "minor"
        }
      ]
    }
  };

  it(
    "should return all rules even empty",
    inject(function(Rules) {
      var sample_response = { rules: [], count: 0 };
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, JSON.stringify(sample_response));
      Rules.getRules().success(function(response) {
        expect(response.count).toEqual(0);
        expect(response.rules).toEqual([]);
      });
      this.$httpBackend.flush();
    })
  );

  it(
    "should return all rules with something",
    inject(function(Rules) {
      var sample_rule = {
        product: "Firefox"
      };
      var sample_response = {
        rules: [sample_rule],
        count: 1
      };
      this.$httpBackend
        .expectGET("/api/rules")
        .respond(200, JSON.stringify(sample_response));
      Rules.getRules().success(function(response) {
        expect(response.count).toEqual(1);
        expect(response.rules[0]).toEqual(sample_rule);
      });
      this.$httpBackend.flush();
    })
  );

  it("should return all rules history",
    inject(function(History) {
      var page = 1;
      var filterParams = {
        objectValue: "rules",
        changedByValue: "hope.ngerebara@gmail.com",
        startDate: 1508923005724,
        endDate: 1508923005755
      };
      this.$httpBackend
      .expectGET("/api/" +filterParams.objectValue +"/history?&page=" +page +
          "&changed_by=" +filterParams.changedByValue +
          "&timestamp_from=" +filterParams.startDate +
          "&timestamp_to=" + filterParams.endDate
      )
        .respond(200, JSON.stringify(sample_rules_response));
      var result = [];
      angular.forEach(sample_rules_response, function(value, key) {
        result.push(value.revisions);
      });
      History.getHistory(filterParams, page).success(function(response) {
        var index = 0;
        angular.forEach(response, function(value, key) {
          expect(value.revisions).toEqual(result[index++]);
        });
      });
      this.$httpBackend.flush();
    })
  );

  it(
    "should return all releases history based the filter option",
    inject(function(History) {
      var sample_releases_response = {
        Releases: {
          count: 2,
          revisions: [
            {
              _different: [],
              _time_ago: "3 days ago",
              change_id: 12635504,
              changed_by: "hope.ngerebara@gmail.com",
              data_version: 798882,
              name: "Firefox-mozilla-central-nightly-latest",
              product: "Firefox",
              read_only: "False",
              timestamp: 1509976085599
            },
            {
              _different: ["data"],
              _time_ago: "3 days ago",
              change_id: 12635482,
              changed_by: "hope.ngerebara@gmail.com",
              data_version: 798881,
              name: "Firefox-mozilla-central-nightly-latest",
              product: "Firefox",
              read_only: "False",
              timestamp: 1509975599716
            }
          ]
        },
        "Releases Scheduled Change": {
          count: 1,
          revisions: [
            {
              change_id: 5,
              change_type: "delete",
              changed_by: "hope.ngerebara@gmail.com",
              complete: true,
              data: null,
              data_version: 1427,
              name: "Devedition-56.0b1-build5",
              product: "Devedition",
              read_only: false,
              sc_data_version: 2,
              sc_id: 2,
              scheduled_by: "balrogadmin",
              timestamp: 1510284736310,
              when: 1510284711868
            }
          ]
        }
      };
      var page = 1;
      var filterParams = {
        objectValue: "releases",
        changedByValue: "hope.ngerebara@gmail.com",
        startDate: 1509976085599,
        endDate: 1510284736310
      };
      var release_sample = [];
      this.$httpBackend
      .expectGET("/api/" +filterParams.objectValue +"/history?&page=" +page +
          "&changed_by=" +filterParams.changedByValue +
          "&timestamp_from=" +filterParams.startDate +
          "&timestamp_to=" + filterParams.endDate
      )
        .respond(200, JSON.stringify(sample_releases_response));
      var result = [];
      angular.forEach(sample_releases_response, function(value, key) {
        result.push(value.revisions);
      });
      History.getHistory(filterParams, page).success(function(response) {
        var index = 0;
        angular.forEach(response, function(value, key) {
          expect(value.revisions).toEqual(result[index++]);
        });
      });
      this.$httpBackend.flush();
    })
  );

  it("should return all Permisions history based the filter option",
    inject(function(History) {
      var sample_permissions_response = {
        "Permissions": {
          "count": 3,
          "revisions": [
            {
              "change_id": 10,
              "changed_by": "hope.ngerebara@gmail.com",
              "data_version": 1,
              "options": {
                "products": [
                  "Widevine"
                ]
              },
              "permission": "admin",
              "timestamp": 1510101325319,
              "username": "test"
            },
            {
              "change_id": 8,
              "changed_by": "hope.ngerebara@gmail.com",
              "data_version": 1,
              "options": {
                "products": [
                  "GMP"
                ]
              },
              "permission": "release",
              "timestamp": 1510100637074,
              "username": "hopez"
            },
          ]
          },
          "Permissions Scheduled Change": {
            "count": 2,
            "revisions": [
              {
                "change_id": 3,
                "change_type": "insert",
                "changed_by": "hope@gmail.com",
                "complete": true,
                "data_version": null,
                "options": {
                  "products": [
                    "GMP"
                  ]
                }
              }
            ]
            }
          }
      var page = 1;
      var filterParams = {
        objectValue: "permissions",
        changedByValue: "hope.ngerebara@gmail.com",
        startDate: 1510101325319,
        endDate: 1510100637074
      };
      this.$httpBackend
      .expectGET("/api/" +filterParams.objectValue +"/history?&page=" +page +
          "&changed_by=" +filterParams.changedByValue +
          "&timestamp_from=" +filterParams.startDate +
          "&timestamp_to=" + filterParams.endDate
      )
        .respond(200, JSON.stringify(sample_permissions_response));
      var result = [];
      angular.forEach(sample_permissions_response, function(value, key) {
        result.push(value.revisions);
      });
      History.getHistory(filterParams, page).success(function(response) {
        var index = 0;
        angular.forEach(response, function(value, key) {
          expect(value.revisions).toEqual(result[index++]);
        });
      });
      this.$httpBackend.flush();
    })
  );

  it("should return all Product signoffs history based the filter option",
  inject(function(History) {
    var sample_product_signoffs_response = {
      "Product Required Signoffs": {
        "count": 1,
        "required_signoffs": [
          {
            "change_id": 2,
            "changed_by": "balrogadmin",
            "channel": "beta-cdntest",
            "data_version": 1,
            "product": "Firefox",
            "role": "releng",
            "signoffs_required": 1,
            "timestamp": 1510100702118
          }
        ]
      },
    }
    var page = 1;
    var filterParams = {
      objectValue: "product_required_signoffs",
      changedByValue: "hope@gmail.com",
      startDate: 1510101325319,
      endDate: 1510100637060
    };
    this.$httpBackend
    .expectGET("/api/" +filterParams.objectValue +"/history?&page=" +page +
        "&changed_by=" +filterParams.changedByValue +
        "&timestamp_from=" +filterParams.startDate +
        "&timestamp_to=" + filterParams.endDate
    )
      .respond(200, JSON.stringify(sample_product_signoffs_response));
    var result = [];
    angular.forEach(sample_product_signoffs_response, function(value, key) {
      result.push(value.revisions);
    });
    History.getHistory(filterParams, page).success(function(response) {
      var index = 0;
      angular.forEach(response, function(value, key) {
        expect(value.revisions).toEqual(result[index++]);
      });
    });
    this.$httpBackend.flush();
  })
);
});
