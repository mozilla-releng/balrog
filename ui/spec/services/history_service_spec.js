describe("Service: History", function() {
    
      beforeEach(function() {
        module("app");
      });
    
      beforeEach(inject(function(History, $httpBackend) {
        this.$httpBackend = $httpBackend;
      }));
    
      afterEach(function() {
        this.$httpBackend.verifyNoOutstandingRequest();
        this.$httpBackend.verifyNoOutstandingExpectation();
      });
    
      it('should return all rules even empty', inject(function(Rules, History) {
        var sample_response = {rules: [], count: 0};
        this.$httpBackend.expectGET('/api/rules')
        .respond(200, JSON.stringify(sample_response));
        Rules.getRules().success(function(response) {
          expect(response.count).toEqual(0);
          expect(response.rules).toEqual([]);
        });
        this.$httpBackend.flush();
      }));
    
      it('should return all rules with something', inject(function(Rules) {
        var sample_rule = {
          product: 'Firefox'
        };
        var sample_response = {
          rules: [sample_rule],
          count: 1,
        };
        this.$httpBackend.expectGET('/api/rules')
        .respond(200, JSON.stringify(sample_response));
        Rules.getRules().success(function(response) {
          expect(response.count).toEqual(1);
          expect(response.rules[0]).toEqual(sample_rule);
        });
        this.$httpBackend.flush();
      }));
      
      var filterParams = {
        objectValue: "rules",
        // changedByValue: ,
        // startDate: $scope.hs_startDate,
        // endDate: $scope.hs_endDate,
        // product: $scope.product,
        // channel: $scope.channel
      };
      it('should return all rules history', inject(function(History) {
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
                    "version": "<56.0.1"
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
                    "version": "<56.0.1"
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
                  "when": 1510700400000
                }
              ]
            }
        };
        
        this.$httpBackend.expectGET('/api/' + filterParams.objectValue +'/history?')
        .respond(200, JSON.stringify(sample_rules_response));
        var result =[];
        angular.forEach(sample_rules_response,function(value,key){
            result.push(value.revisions);
        })
        History.getHistory(filterParams).success(function(response) {
            var index = 0;
            angular.forEach(response, function(value, key){
                // console.log(result[index], index)
                // console.log('***************')
                // expect(value.count).toEqual(2);
                expect(value.revisions).toEqual(result[index++]);
            })
        });
        this.$httpBackend.flush();
      }));
    
    //   it('should return an individual rule', inject(function(Rules) {
    //     var sample_response = {
    //       change_id: 123,
    //       product: "Firefox",
    //       data_version: 3,
    //     };
    //     this.$httpBackend.expectGET('/api/rules/1')
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.getRule(1).success(function(response) {
    //       expect(response).toEqual(sample_response);
    //     });
    //     this.$httpBackend.flush();
    //   }));
    
    //   it('should update an individual rule', inject(function(Rules) {
    //     var sample_response = {
    //       new_data_version: 4,
    //     };
    //     this.$httpBackend.expectPUT('/api/rules/1')
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.updateRule(1, {}).success(function(response) {
    //       expect(response).toEqual(sample_response);
    //     });
    //     this.$httpBackend.flush();
    //   }));
    
    //   it('should be to delete an individual rule', inject(function(Rules) {
    //     var sample_response = {
    //       new_data_version: 4,
    //     };
    //     var delete_url = '/api/rules/1?data_version=123&csrf_token=mytoken'
    //     this.$httpBackend.expectDELETE(delete_url)
    //     .respond(200, '');
    //     Rules.deleteRule(1, {data_version: 123}, 'mytoken')
    //     .success(function(response) {
    //       expect(response).toEqual('');
    //     });
    //     this.$httpBackend.flush();
    //   }));
    
    //   it('should be able to add an invidual rule', inject(function(Rules) {
    //     this.$httpBackend.expectPOST('/api/rules')
    //     .respond(200, '123');
    //     Rules.addRule({product: "firefox"}, 'mytoken')
    //     .success(function(response) {
    //       expect(response).toEqual('123');
    //     });
    //     this.$httpBackend.flush();
    //   }));
    
    //   it('should be able to add an revert a rule', inject(function(Rules) {
    //     var url = '/api/rules/123/revisions';
    //     this.$httpBackend.expectPOST(url)
    //     .respond(200, '');
    //     Rules.revertRule(123, 987, 'mytoken')
    //     .success(function(response) {
    //       expect(response).toEqual('');
    //     });
    //     this.$httpBackend.flush();
    //   }));
    
    //   it("should return all scheduled rule changes", inject(function(Rules) {
    //     var sample_sc = {
    //       "sc_id": 1,
    //       "scheduled_by": "jess",
    //       "complete": false,
    //       "when": new Date(123456789),
    //       "base_rule_id": 2,
    //       "base_product": "Firefox",
    //       "base_channel": "release",
    //       "base_data_version": 1
    //     };
    //     var sample_response = {
    //       count: 1,
    //       scheduled_changes: [sample_sc]
    //     };
    //     this.$httpBackend.expectGET("/api/scheduled_changes/rules?all=1")
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.getScheduledChanges().success(function(response) {
    //       expect(response.count).toEqual(1);
    //       expect(response.scheduled_changes[0]).toEqual(sample_sc);
    //     });
    //   }));
    
    //   it("should return a single scheduled rule change", inject(function(Rules) {
    //     var sample_response = {
    //       "sc_id": 1,
    //       "scheduled_by": "jess",
    //       "complete": false,
    //       "when": new Date(123456789),
    //       "base_rule_id": 2,
    //       "base_product": "Firefox",
    //       "base_channel": "release",
    //       "base_data_version": 1
    //     };
    //     this.$httpBackend.expectGET("/api/scheduled_changes/rules/1")
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.getScheduledChange(1).success(function(response) {
    //       expect(response).toEqual(sample_response);
    //     });
    //   }));
    
    //   it("should be able to create a scheduled change", inject(function(Rules) {
    //     var sample_response = {
    //       sc_id: 1
    //     };
    //     this.$httpBackend.expectPOST("/api/scheduled_changes/rules")
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.addScheduledChange({"when": new Date(123456789), "base_product": "Foo"}, "csrf").success(function(response) {
    //       expect(response.sc_id).toEqual(1);
    //     });
    //   }));
    
    //   it("should be able to update a scheduled change", inject(function(Rules) {
    //     var sample_response = {
    //       new_data_version: 2
    //     };
    //     this.$httpBackend.expectPOST("/api/scheduled_changes/rules/2")
    //     .respond(200, JSON.stringify(sample_response));
    //     Rules.updateScheduledChange(2, {"when": new Date(123456789), "base_mapping": "abc", "data_version": 1}, "csrf")
    //     .success(function(response) {
    //       expect(response).toEqual(sample_response);
    //     });
    //   }));
    
    //   it("should be able to delete a scheduled change", inject(function(Rules) {
    //     this.$httpBackend.expectDELETE("/api/scheduled_changes/rules/3?data_version=2&csrf_token=csrf")
    //     .respond(200);
    //     Rules.deleteScheduledChange(3, {sc_data_version: 2}, "csrf");
    //   }));
    
    //   // todo: add sc history methods
    
    //   it("should respect both old and new rule", inject(function(Rules) {
    //     var signoffRequirements = [
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //       {product: "Firefox", channel: "release", role: "relman", signoffs_required: 4},
    //     ];
    //     var oldRule = {product: "Firefox", channel: "nightly", mapping: "Firefox"};
    //     var newRule = {product: "Firefox", channel: "release", mapping: "Firefox"};
    //     var signoffsRequired = Rules.ruleSignoffsRequired(oldRule, newRule, signoffRequirements);
    //     expect(signoffsRequired.length).toBe(2);
    //     expect(signoffsRequired.roles['releng']).toBe(2);
    //     expect(signoffsRequired.roles['relman']).toBe(4);
    //   }));
    
    //   it("should take maximum of required signoffs", inject(function(Rules) {
    //     var signoffRequirements = [
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //       {product: "Firefox", channel: "nightly", role: "relman", signoffs_required: 4},
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 3},
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //     ];
    //     var rule = {product: "Firefox", channel: "nightly", mapping: "Firefox"};
    //     var signoffsRequired = Rules.ruleSignoffsRequired(rule, undefined, signoffRequirements);
    //     expect(signoffsRequired.length).toBe(2);
    //     expect(signoffsRequired.roles['releng']).toBe(3);
    //     expect(signoffsRequired.roles['relman']).toBe(4);
    //   }));
    
    //   it("should match globs", inject(function(Rules) {
    //     var signoffRequirements = [
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //     ];
    //     var rule = {product: "Firefox", channel: "night*", mapping: "Firefox"};
    //     var signoffsRequired = Rules.ruleSignoffsRequired(rule, undefined, signoffRequirements);
    //     expect(signoffsRequired.length).toBe(1);
    //     expect(signoffsRequired.roles['releng']).toBe(2);
    //   }));
    
    //   it("should match missing channels against all channels", inject(function(Rules) {
    //     var signoffRequirements = [
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //       {product: "Firefox", channel: "release", role: "relman", signoffs_required: 2},
    //       {product: "Firefox", channel: "esr", role: "admin", signoffs_required: 2},
    //     ];
    //     var rule = {product: "Firefox", mapping: "Firefox"};
    //     var signoffsRequired = Rules.ruleSignoffsRequired(rule, undefined, signoffRequirements);
    //     expect(signoffsRequired.length).toBe(3);
    //     expect(signoffsRequired.roles['releng']).toBe(2);
    //     expect(signoffsRequired.roles['relman']).toBe(2);
    //     expect(signoffsRequired.roles['admin']).toBe(2);
    //   }));
    
    //   it("should match only if both product and channel match", inject(function(Rules) {
    //     var signoffRequirements = [
    //       {product: "Firefox", channel: "nightly", role: "releng", signoffs_required: 2},
    //     ];
    //     var rule = {product: "Firefox", channel: "aurora", mapping: "Firefox"};
    //     var signoffsRequired = Rules.ruleSignoffsRequired(rule, undefined, signoffRequirements);
    //     expect(signoffsRequired.length).toBe(0);
    //   }));
    });
    