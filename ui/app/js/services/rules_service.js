angular.module("app").factory('Rules', function($http, ScheduledChanges, Helpers, ProductRequiredSignoffs) {
  // these routes map to stubbed API endpoints in config/server.js
  var service = {
    getRules: function() {
      return $http.get('/api/rules');
    },
    getChannels: function(){
      return $http.get('/api/rules/columns/channel');
    },
    getProducts: function(){
      return $http.get('/api/rules/columns/product');
    },

    getHistory: function(id, limit, page) {
      return $http.get('/api/rules/' + id + '/revisions?limit=' + limit + '&page=' + page);
    },
    getRule: function(id) {
      return $http.get('/api/rules/' + id);
    },
    updateRule: function(id, data, csrf_token) {
      data.csrf_token = csrf_token;
      data = Helpers.replaceEmptyStrings(data);
      return $http.put('/api/rules/' + id, data);
    },
    deleteRule: function(id, data, csrf_token) {
      var url = '/api/rules/' + id;
      url += '?data_version=' + data.data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    addRule: function(data, csrf_token) {
      data.csrf_token = csrf_token;
      data = Helpers.replaceEmptyStrings(data);
      return $http.post('/api/rules', data);
    },
    revertRule: function(id, change_id, csrf_token) {
      var data = {change_id: change_id};
      data.csrf_token = csrf_token;
      return $http.post('/api/rules/' + id + '/revisions', data);
    },
    getScheduledChanges: function(all) {
      if (all === undefined || all === true) {
        return $http.get("/api/scheduled_changes/rules?all=1");
      }
      else {
        return $http.get("/api/scheduled_changes/rules");
      }
    },
    getScheduledChange: function(sc_id) {
      return $http.get("/api/scheduled_changes/rules/" + sc_id);
    },
    addScheduledChange: function(data, csrf_token) {
      data = jQuery.extend({}, data);
      data = Helpers.replaceEmptyStrings(data);
      if (!!data.when) {
        data.when = data.when.getTime();
      }else{
          data.when = null;
      }
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/rules", data);
    },
    getScheduledChangeHistory: function(sc_id, limit, page) {
      return $http.get('/api/scheduled_changes/rules/' + sc_id + '/revisions?limit=' + limit + '&page=' + page);
    },
    updateScheduledChange: function(sc_id, data, csrf_token) {
      data = jQuery.extend({}, data);
      data = Helpers.replaceEmptyStrings(data);
      if (!!data.when) {
        data.when = data.when.getTime();
      }
      else {
        data.when = null;
      }
      data.csrf_token = csrf_token;
      return $http.post("/api/scheduled_changes/rules/" + sc_id, data);
    },
    deleteScheduledChange: function(sc_id, data, csrf_token) {
      var url = "/api/scheduled_changes/rules/" + sc_id;
      url += '?data_version=' + data.sc_data_version;
      url += '&csrf_token=' + encodeURIComponent(csrf_token);
      return $http.delete(url);
    },
    signoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("rules", sc_id);
      return $http.post(url, data);
    },
    revokeSignoffOnScheduledChange: function(sc_id, data) {
      var url = ScheduledChanges.signoffsUrl("rules", sc_id);
      url += "?csrf_token=" + encodeURIComponent(data["csrf_token"]);
      return $http.delete(url, data);
    },
    ruleSignoffsRequired: function(oldRule, newRule, productSignoffRequirements) {
      // Limited support for the only globs that we encounter in
      // balrog, which are of the form "foo*".
      function matchGlob(glob, target) {
        if (glob[glob.length-1] === '*') {
          return target.slice(0, glob.length-1) === glob.slice(0, glob.length-1);
        }
        return target === glob;
      }

      // Identify signoffs matching oldRule and newRule
      function matchesRule(rule, signOffRequirement) {
        if (rule.product && signOffRequirement.product !== rule.product) {
          return false;
        }
        if (rule.channel && !matchGlob(rule.channel, signOffRequirement.channel)) {
          return false;
        }
        return true;
      }
      function matchesRules(signOffRequirement) {
        var rules = [];
        // Don't check old rule if we're newly creating a rule.
        if (oldRule) {
          rules.push(oldRule);
        }
        // Don't check new rule if we're deleting a rule.
        if (newRule) {
          rules.push(newRule);
        }
        return rules.some(function(rule) { return matchesRule(rule, signOffRequirement); });
      }

      var relevantRequirements = productSignoffRequirements.filter(matchesRules);
      return ProductRequiredSignoffs.convertToMap(relevantRequirements);
    },
  };
  return service;

});
