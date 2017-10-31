// describe("controller: HistoryController", function() {
    
//       beforeEach(function() {
//         module("app");
//       });

//       beforeEach(inject(function($controller, $rootScope, History, $httpBackend) {
//         this.$httpBackend = $httpBackend;
//         this.scope = $rootScope.$new();
//         $controller('HistoryController', {
//           $scope: this.scope,
//           History: History
//         });
//       }));
    
//       afterEach(function() {
//         this.$httpBackend.verifyNoOutstandingRequest();
//         this.$httpBackend.verifyNoOutstandingExpectation();
//       });
      
//       var sample_rules_response = {
//         "Rules": {
//             "count": 2,
//             "revisions": [
//               {
//                 "alias": null,
//                 "backgroundRate": 100,
//                 "buildID": null,
//                 "buildTarget": "WINNT_x86-msvc-x64",
//                 "change_id": 9490,
//                 "changed_by": "sfraser@mozilla.com",
//                 "channel": "release-cdntest",
//                 "comment": "Watershed rule to update 56.0 win32 users who are eligible for win64 to 56.0.2",
//                 "data_version": 3,
//                 "distVersion": null,
//                 "distribution": null,
//                 "fallbackMapping": null,
//                 "headerArchitecture": null,
//                 "instructionSet": null,
//                 "jaws": null,
//                 "locale": null,
//                 "mapping": "Firefox-56.0.2-build1-win64-migration-WNP",
//                 "memory": ">2048",
//                 "mig64": true,
//                 "osVersion": null,
//                 "priority": 94,
//                 "product": "Firefox",
//                 "rule_id": 665,
//                 "timestamp": 1508923005724,
//                 "update_type": "minor",
//                 "version": "<56.0.1"
//               },
//               {
//                 "alias": null,
//                 "backgroundRate": 100,
//                 "buildID": null,
//                 "buildTarget": null,
//                 "change_id": 9489,
//                 "changed_by": "sfraser@mozilla.com",
//                 "channel": "release-cdntest",
//                 "comment": "Show mobile promotion WNP to users who stayed on 56.0 (win64-migrated users have already seen it in 56.0.1)",
//                 "data_version": 2,
//                 "distVersion": null,
//                 "distribution": null,
//                 "fallbackMapping": null,
//                 "headerArchitecture": null,
//                 "instructionSet": null,
//                 "jaws": null,
//                 "locale": null,
//                 "mapping": "Firefox-56.0.2-build1-WNP",
//                 "memory": null,
//                 "mig64": null,
//                 "osVersion": null,
//                 "priority": 92,
//                 "product": "Firefox",
//                 "rule_id": 666,
//                 "timestamp": 1508923005671,
//                 "update_type": "minor",
//                 "version": "<56.0.1"
//               }
//             ]
//         },
//         "Rules scheduled change": {
//           "count": 1,
//           "revisions": [
//             {
//               "alias": null,
//               "backgroundRate": 0,
//               "buildID": ">=20170730030209",
//               "buildTarget": null,
//               "change_id": 2,
//               "change_type": "update",
//               "changed_by": "balrogadmin",
//               "channel": "nightlytest",
//               "comment": "bug 1386230 For all builds after 20170731030207 renable updates to latest nightly.",
//               "complete": false,
//               "data_version": 2,
//               "distVersion": null,
//               "distribution": null,
//               "fallbackMapping": null,
//               "headerArchitecture": null,
//               "instructionSet": null,
//               "jaws": null,
//               "locale": null,
//               "mapping": "Thunderbird-comm-central-nightly-latest",
//               "memory": null,
//               "mig64": null,
//               "osVersion": null,
//               "priority": 89,
//               "product": "Thunderbird",
//               "rule_id": 633,
//               "sc_data_version": 1,
//               "sc_id": 1,
//               "scheduled_by": "balrogadmin",
//               "telemetry_channel": null,
//               "telemetry_product": null,
//               "telemetry_uptake": null,
//               "timestamp": 1509379903963,
//               "update_type": "minor",
//               "version": null,
//               "when": 1510700400000
//             }
//           ]
//         }
//       };

//       var sample_scheduled_change = {
//         "releases_scheduled_change": {
//             "count": 1,
//             "revisions": [
//               {
//                 "change_id": 2,
//                 "change_type": "delete",
//                 "changed_by": "balrogadmin",
//                 "complete": false,
//                 "data": null,
//                 "data_version": 1392,
//                 "name": "Firefox-53.0.3-build1",
//                 "product": "Firefox",
//                 "read_only": false,
//                 "sc_data_version": 1,
//                 "sc_id": 1,
//                 "scheduled_by": "balrogadmin",
//                 "timestamp": 1509012699166,
//                 "when": 1509404400000
//               }
//             ]
//           }
//       }

//     //   var checkboxValues = {rules: 0, releases:0, permissions:0 };
//     //   var result = {
//     //     changedByValue: "",
//     //     startDate: 1509012699166,
//     //     endDate: 1508923005724
//     //   };
    
      
    
//       describe("fetching all History", function() {
//         it("should return an array based on the tab and checkboxes selected", function() {
//             this.$httpBackend.expectGET('/api/rules')
//             .respond(200, '{"rules": [], "count": 0}');
//             this.$httpBackend.expectGET('/api/rules/columns/product')
//             .respond(200, JSON.stringify({product: ['Product1', 'Product2'], count: 2}));
//             this.$httpBackend.expectGET('/api/rules/columns/channel')
//             .respond(200, JSON.stringify({channel: ['Channel1', 'Channel2'], count: 2}));
//             this.$httpBackend.expectGET('/api/rules/history')
//             .respond(200, JSON.stringify(sample_rules_response)); 
//             // this.$httpBackend.expectGET('/api/rrp/history?rules=1&releases=0&permissions=0')
//             // .respond(200, JSON.stringify(sample_rules));
//             // this.$httpBackend.expectGET('/api/sc/history?rules_scheduled_change=0&releases_scheduled_change=0&permissions_scheduled_change=0&permissions_required_signoff_scheduled_change=0&product_required_signoff_scheduled_change=0')
//             // .respond(200,'{}')
//             // this.$httpBackend.expectGET('/api/required_signoff/history?permissions_required_signoffs=0&product_required_signoffs=0')
//             // .respond(200, '{}')
//             this.$httpBackend.flush();
//             console.log('called');
//         });   

//       //   it("should return an array based on the tab and checkboxes selected", function() { 
//       //     this.$httpBackend.whenGET('/api/rrp/history?rules=1&releases=1&permissions=1')
//       //     .respond(200, JSON.stringify(sample_rrp_response)); 
//       //     this.$httpBackend.whenGET('/api/rrp/history?rules=1&releases=0&permissions=0')
//       //     .respond(200, JSON.stringify(sample_rules));
//       //     this.$httpBackend.expectGET('/api/sc/history?permissions_required_signoff_scheduled_change=1')
//       //     .respond(200,'{"permissions_required_signoff_scheduled_change": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/sc/history?product_required_signoff_scheduled_change=1')
//       //     .respond(200,'{"permissions_scheduled_change": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/sc/history?permissions_scheduled_change=1')
//       //     .respond(200,'{"permissions_scheduled_change": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/sc/history?releases_scheduled_change=1')
//       //     .respond(200,'{"releases_scheduled_change": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/sc/history?rules_scheduled_change=1')
//       //     .respond(200,'{"rules_scheduled_change": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/required_signoff/history?permissions_required_signoff=1')
//       //     .respond(200, '{"permissions_required_signoff": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.expectGET('/api/required_signoff/history?product_required_signoff=1')
//       //     .respond(200, '{"product_required_signoff": {"count": 0, "revisions": []}')
//       //     this.$httpBackend.flush();
//       //     console.log(this.$scope.rules.revisions,'called');            
//       //     expect(this.$scope.rules.revisions).toEqual([]);
//       //     expect(this.$scope.rules.revisions).toEqual([]);
//       //     expect(this.$scope.rules.revisions).toEqual([]);
//       // });   
//       });

//     //   describe("Filters", function() {
//     //       it("should be possible to search with a specific username or email", function() {
//     //         this.$httpBackend.expectGET('/api/rrp/history?rules=1&changed_by=sfraser@mozilla.com')
//     //         .respond(200, JSON.stringify(sample_rules));
//     //       })
//     //       it("should be possible to search with a specific username and date range ", function() {
//     //         this.$httpBackend.expectGET('/api/rrp/history?rules=1&changed_by=sfraser@mozilla.com&timestamp_from=1508923005671&timestamp_to=1508923005724')
//     //         .respond(200, JSON.stringify(sample_rules));
//     //       })
//     //   })

    
//     //   describe('opening modals', function() {
//     //     it("should be possible to open the modal for each rule object", function() {
//     //         this.$httpBackend.expectGET('/api/rrp/history?rules=1&changed_by=sfraser@mozilla.com')
//     //         .respond(200, JSON.stringify(sample_rules));   
//     //         this.scope.openDataModal(sample_rules.rules.revisions[0].change_id);
//     //     });
//     //     it("should be possible to open the modal for each rule object", function() {
//     //         this.$httpBackend.expectGET('/api/sc/history?releases_scheduled_change=1&changed_by=balrogadmin')
//     //         .respond(200, JSON.stringify(sample_scheduled_change));   
//     //         this.scope.openDataModal(sample_scheduled_change.releases_scheduled_change.revisions[0].change_id);
//     //     });
//     //   });
//     });
    
    