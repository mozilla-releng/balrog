describe("controller: HistoryController", function() {
  
    beforeEach(function() {
      module("app");
    });
    var changed_by_response = {
      "changed_by": "testemail1@mozilla.com",
      "channel": "release-cdntest",
    }
    var sample_rules_response = {
      "Rules": {
          "count": 2,
          "revisions": [
            {
              "alias": null,
              "backgroundRate": 100,
              "buildID": null,
              "buildTarget": "WINNT_x86-msvc-x64",
              "change_id": 9490,
              "changed_by": "testemail1@mozilla.com",
              "channel": "release-cdntest",
              "comment": "Watershed rule to update 56.0 win32 users who are eligible for win64 to 56.0.2",
              "data_version": 3,
              "distVersion": null,
              "distribution": null,
              "fallbackMapping": null,
              "headerArchitecture": null,
              "instructionSet": null,
              "jaws": null,
              "locale": null,
              "mapping": "Firefox-56.0.2-build1-win64-migration-WNP",
              "memory": ">2048",
              "mig64": true,
              "osVersion": null,
              "priority": 94,
              "product": "Firefox",
              "rule_id": 665,
              "timestamp": 1508923005724,
              "update_type": "minor",
              "version": "<56.0.1",
              type : 'Rules'
            },
            {
              "alias": null,
              "backgroundRate": 100,
              "buildID": null,
              "buildTarget": null,
              "change_id": 9489,
              "changed_by": "testemail2@mozilla.com",
              "channel": "release-cdntest",
              "comment": "Show mobile promotion WNP to users who stayed on 56.0 (win64-migrated users have already seen it in 56.0.1)",
              "data_version": 2,
              "distVersion": null,
              "distribution": null,
              "fallbackMapping": null,
              "headerArchitecture": null,
              "instructionSet": null,
              "jaws": null,
              "locale": null,
              "mapping": "Firefox-56.0.2-build1-WNP",
              "memory": null,
              "mig64": null,
              "osVersion": null,
              "priority": 92,
              "product": "Firefox",
              "rule_id": 666,
              "timestamp": 1508923005671,
              "update_type": "minor",
              "version": "<56.0.1",
              type : 'Rules'
            }
          ]
      },
      "Rules scheduled change": {
        "count": 1,
        "revisions": [
          {
            "alias": null,
            "backgroundRate": 0,
            "buildID": ">=20170730030209",
            "buildTarget": null,
            "change_id": 2,
            "change_type": "update",
            "changed_by": "balrogadmin",
            "channel": "nightlytest",
            "comment": "bug 1386230 For all builds after 20170731030207 renable updates to latest nightly.",
            "complete": false,
            "data_version": 2,
            "distVersion": null,
            "distribution": null,
            "fallbackMapping": null,
            "headerArchitecture": null,
            "instructionSet": null,
            "jaws": null,
            "locale": null,
            "mapping": "Thunderbird-comm-central-nightly-latest",
            "memory": null,
            "mig64": null,
            "osVersion": null,
            "priority": 89,
            "product": "Thunderbird",
            "rule_id": 633,
            "sc_data_version": 1,
            "sc_id": 1,
            "scheduled_by": "balrogadmin",
            "telemetry_channel": null,
            "telemetry_product": null,
            "telemetry_uptake": null,
            "timestamp": 1509379903963,
            "update_type": "minor",
            "version": null,
            "when": 1510700400000,
            type : 'Rules scheduled change'
          }
        ]
      }
    };

    var sample_releases_response = {
      "Releases": {
        "count": 3,
        "revisions": [
          {
            "_different": [],
            "_time_ago": "1 day ago",
            "change_id": 12635504,
            "changed_by": "balrog-ffxbld",
            "data_version": 798882,
            "name": "Firefox-mozilla-central-nightly-latest",
            "product": "Firefox",
            "read_only": "False",
            "timestamp": 1509976085599
          },
          {
            "_different": [
              "name",
              "data"
            ],
            "_time_ago": "13 days ago",
            "change_id": 12598209,
            "changed_by": "balrog-ffxbld",
            "data_version": 1101,
            "name": "Firefox-56.0.2-build1",
            "product": "Firefox",
            "read_only": "False",
            "timestamp": 1508945131597
          },
          {
            "_different": [
              "name",
              "data"
            ],
            "_time_ago": "13 days ago",
            "change_id": 12598208,
            "changed_by": "balrog-ffxbld",
            "data_version": 1100,
            "name": "Firefox-56.0.2-build1",
            "product": "Firefox",
            "read_only": "False",
            "timestamp": 1508945125164
          }
        ]
      },
      "Releases scheduled change": {
        "count": 0,
        "revisions": []
      }
    }
  var $scope;
  beforeEach(inject(function($controller, $rootScope, History, $httpBackend) {
    this.$httpBackend = $httpBackend;
    this.scope = $rootScope.$new();
    $controller('HistoryController', {
      $scope: this.scope,
      History: History
    });
    // $scope = this.scope;
  }));

  afterEach(function() {
    this.$httpBackend.verifyNoOutstandingRequest();
    this.$httpBackend.verifyNoOutstandingExpectation();
  });

  describe("fetching all History", function() {
      it("should return an empty search result", function() {
          this.$httpBackend.expectGET('/api/rules')
          .respond(200, '{"rules": [], "count": 0}');
          this.$httpBackend.expectGET('/api/rules/columns/product')
          .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
          this.$httpBackend.expectGET('/api/rules/columns/channel')
          .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
          this.$httpBackend.flush();
          expect(this.scope.searchResult).toEqual([]);
      });  
  })

  describe("Filters", function() {
      it("should return the response when 'rules' object is selected", function()  {  
        this.scope.data.objectSelected = {id: '2', name: 'rules', value: 'Rules'};
        this.scope.searchHistory(); 
        this.$httpBackend.expectGET('/api/rules')
        .respond(200, '{"rules": [], "count": 0}');
        this.$httpBackend.expectGET('/api/rules/history?')
        .respond(200, JSON.stringify({"Rules": {"count": 2,"revisions": ['test','test2']},"Rules Scheduled Change": {"count": 1,"revisions": []}})); 
        this.$httpBackend.expectGET('/api/rules/columns/product')
        .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
        this.$httpBackend.expectGET('/api/rules/columns/channel')
        .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
        this.$httpBackend.flush();
        expect(this.scope.searchResult).toEqual(['test','test2']);
      })

      it("should return the response when the changed_by name is entered", function()  {  
        this.scope.data.objectSelected = {id: '2', name: 'rules', value: 'Rules'};
        this.scope.userInput.changedBy = 'testemail1@mozilla.com';
        this.scope.searchHistory(); 
        var parent = this;
        this.$httpBackend.expectGET('/api/rules')
        .respond(200, '{"rules": [], "count": 0}');
        var result = [];
        angular.forEach(sample_rules_response, function(value,key){
          result.push(value.revisions)
        })
        this.$httpBackend.expectGET('/api/rules/history?&changed_by=testemail1@mozilla.com')
        .respond(200, JSON.stringify(sample_rules_response));
        this.$httpBackend.expectGET('/api/rules/columns/product')
        .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
        this.$httpBackend.expectGET('/api/rules/columns/channel')
        .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
        
        // this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com&timestamp_from=1508923005671&timestamp_to=1508923005724')
          // .respond(200, JSON.stringify(sample_rules));
          // this.$httpBackend.expectGET('/api/rules/history?product="Firefox&channel="beta')
          // .respond(200, JSON.stringify(sample_rules));
          this.$httpBackend.flush();
          console.log(this.scope.searchResult,"$scope.searchResult");
          expect(this.scope.searchResult[0]).toEqual(result[0]);
          // expect(this.scope.searchResult).toEqual(['test','test2']);
      })
      // it("should return the response when 'release' object is selected", function()  {     
      //     console.log($scope.objectValue,"$scope.objectValue===========")
      //     this.$httpBackend.expectGET('/api/releases/history')
      //     .respond(200, JSON.stringify(sample_rules_response)); 
      //     this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com')
      //     .respond(200, JSON.stringify(sample_rules));
      //     this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com&timestamp_from=1508923005671&timestamp_to=1508923005724')
      //     .respond(200, JSON.stringify(sample_rules));
      //     this.$httpBackend.expectGET('/api/rules/history?product="Firefox&channel="beta')
      //     .respond(200, JSON.stringify(sample_rules));
      // })

      // it("should return the response when 'permissions' object is selected", function()  {     
      //     this.$httpBackend.expectGET('/api/permissions/history')
      //     .respond(200, JSON.stringify(sample_rules_response)); 
      //     this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com')
      //     .respond(200, JSON.stringify(sample_rules));
      //     this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com&timestamp_from=1508923005671&timestamp_to=1508923005724')
      //     .respond(200, JSON.stringify(sample_rules));
      //     this.$httpBackend.expectGET('/api/rules/history?product="Firefox&channel="beta')
      //     .respond(200, JSON.stringify(sample_rules));
      // })
  });   

  // describe('opening modals', function() {
  //     it("should be possible to open the modal for each rule object instance", function() {
  //         this.$httpBackend.expectGET('/api/rules/history?changed_by=sfraser@mozilla.com')
  //         .respond(200, JSON.stringify(sample_rules));   
  //         this.scope.openDataModal(sample_rules.rules.revisions[0].change_id);
  //     });
  //     it("should be possible to open the modal for each release object instance", function() {
  //         this.$httpBackend.expectGET('/api/release/history?changed_by=balrogadmin')
  //         .respond(200, JSON.stringify(sample_scheduled_change));   
  //         this.scope.openDataModal(sample_scheduled_change.releases_scheduled_change.revisions[0].change_id);
  //     });     
  // });
});
  
  