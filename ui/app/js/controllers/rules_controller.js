angular.module("app").controller('RulesController',
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route, Releases, Page, Permissions, ProductRequiredSignoffs, Helpers) {

  Page.setTitle('Rules');

  $scope.loading = true;
  $scope.failed = false;

  $scope.rule_id = parseInt($routeParams.id, 10);
  $scope.pr_ch_options = [];
  $scope.currentPage = 1;
  $scope.storedPageSize = JSON.parse(localStorage.getItem('rules_page_size'));
  $scope.pageSize = $scope.storedPageSize? $scope.storedPageSize.id : 20;
  $scope.page_size = {id: $scope.pageSize, name: $scope.storedPageSize? $scope.storedPageSize.name : $scope.pageSize};
  $scope.maxSize = 10;
  $scope.rules = [];
  $scope.pr_ch_filter = "";
  $scope.show_sc = true;

  function changeLocationWithFilterParams(filterParamsString) {
    localStorage.setItem("pr_ch_filter", filterParamsString);
    var pr_ch_array = filterParamsString.split(',');
    if (pr_ch_array[0].toLowerCase() === "all rules" || $scope.rule_id) {
      $location.path('/rules').search({});
    } else if (pr_ch_array && pr_ch_array.length > 1) {
      $location.path('/rules').search({ product: pr_ch_array[0], channel: pr_ch_array[1] });
    } else {
      $location.path('/rules').search({ product: pr_ch_array[0] });
    }
  }

  if($location.url().split('=')[1]) {
    var urlParams = "";
    $location.url().split('?')[1].split('&').map(function(str) { 
      if(urlParams.length > 1) {
        urlParams += ',';
        urlParams += str.split('=')[1];
      } else {
        urlParams += str.split('=')[1];
      }
    });
    changeLocationWithFilterParams(urlParams);
  } 

  function loadPage(newPage) {
    Rules.getHistory($scope.rule_id, $scope.pageSize, newPage)
    .success(function(response) {
      $scope.rules = response.rules;
      $scope.rules_count = response.count;
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  if ($scope.rule_id) {
    // history of a specific rule
    $scope.$watch("currentPage", function(newPage) {
      loadPage(newPage);
    });
  } else {
    Rules.getRules()
    .success(function(response) {
      $scope.rules_count = response.count;
      $scope.page_size_pair = [{id: 20, name: '20'},
        {id: 50, name: '50'}, 
        {id: $scope.rules_count, name: 'All'}];

      Permissions.getCurrentUser()
      .success(function(response) {
        $scope.current_user = response["username"];
        $scope.user_roles = Object.keys(response["roles"]);
      })
      .error(function(response) {
        sweetAlert(
          "Failed to load current user Roles:",
          response
        );
      });

      Rules.getScheduledChanges(false)
      .success(function(sc_response) {
        response.rules.forEach(function(rule) {
          rule.scheduled_change = null;
          sc_response.scheduled_changes.forEach(function(sc) {
            if (rule.rule_id === sc.rule_id) {
              // Note the big honking assumption that there's only one scheduled change.
              // At the time this code was written, this was enforced by the backend.
              rule.scheduled_change = sc;
              rule.scheduled_change.when = new Date(rule.scheduled_change.when);
            }
          });
          $scope.rules.push(rule);
        });
        sc_response.scheduled_changes.forEach(function(sc) {
          if (sc.change_type === "insert") {
            var rule = {"scheduled_change": sc};
            rule.scheduled_change.when = new Date(rule.scheduled_change.when);
            $scope.rules.push(rule);
          }
        });
      });

      var pairExists = function(pr, ch) {
        var _rules = $scope.rules.filter(function(rule) {
          return rule.product === pr && rule.channel === ch;
        });
        return _rules.length !== 0;
      };
      Rules.getProducts().success(function(response_prs) {
        Rules.getChannels().success(function(response_chs) {
          response_prs.product.forEach(function(pr) {
            $scope.pr_ch_options.push(pr);
            response_chs.channel.forEach(function(ch) {
              if (ch.indexOf("*") === -1 && pairExists(pr, ch)){
                var pr_ch_pair = pr.concat(",").concat(ch);
                $scope.pr_ch_options.push(pr_ch_pair);
              }
            });
          });
        })
        .finally(function() {
          $scope.pr_ch_options.sort().unshift("All rules");
          $scope.pr_ch_filter = "All rules";
          if ($scope.pr_ch_options.includes(localStorage.getItem('pr_ch_filter'))){
            $scope.pr_ch_filter = localStorage.getItem('pr_ch_filter') || "All rules";
          }
        });
      });

      ProductRequiredSignoffs.getRequiredSignoffs()
        .then(function(payload) {
        $scope.signoffRequirements = payload.data.required_signoffs;
      });
      $scope.ruleSignoffsRequired = function(rule) {
        if ($scope.signoffRequirements) {
          return Rules.ruleSignoffsRequired(rule, undefined, $scope.signoffRequirements);
        }
      };
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

  $scope.$watch('pr_ch_filter', function(value) {
    if (value) {
      localStorage.setItem("pr_ch_filter", value);
    }
    $scope.pr_ch_selected = value.split(',');
  });

  $scope.selectPageSize = function() {
    Helpers.selectPageSize($scope, 'rules_page_size');
  };

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };

  $scope.orderRules = function(rule) {
    // Rules are sorted by priority. Rules that are pending (ie: still just a Scheduled Change)
    // will be inserted based on the priority in the Scheduled Change.
    // Rules that have Scheduled updates or deletes will remain sorted on their current priority
    // because it's more important to make it easy to assess current state than future state.
    if (rule.priority === null || rule.priority === undefined) {
        return rule.scheduled_change.priority * -1;
    }
    else {
        return rule.priority * -1;
    }
  };

  $scope.channelMatchesRule = function(channel, rule) {
    if (rule.channel === channel) {
      return true;
    }
    if (rule.channel.indexOf("*") > -1 && channel.startsWith(rule.channel.split("*")[0])) {
      return true;
    }
  };

  $scope.filterBySelect = function(rule) {
    // Always return all entries if "all rules" is the filter
    // or if $scope.rule_id is set (meaning we're on the history page).
    if ($scope.pr_ch_selected[0].toLowerCase() === "all rules" || $scope.rule_id) {
      return true;
    }
    else if ($scope.pr_ch_selected && $scope.pr_ch_selected.length > 1) {
      selected_product = $scope.pr_ch_selected[0];
      selected_channel = $scope.pr_ch_selected[1];
      productMatches = false;
      channelMatches = false;
      if (rule.product === null || rule.product === "" || rule.product === selected_product) {
        productMatches = true;
      }
      if ($scope.show_sc && rule.scheduled_change !== null) {
        // If product is null in the Scheduled Change it could be because it is
        // changing to null, or because the Rule is scheduled to be deleted.
        // In the latter case, we don't consider it a match, because that will
        // cause it to show up on the views of _all_ products.
        if (rule.scheduled_change.product === selected_product ||
            (rule.scheduled_change.change_type !== "delete" && !rule.scheduled_change.product)) {
          productMatches = true;
        }
      }
      if (rule.channel === null || rule.channel === "" || (rule.channel && $scope.channelMatchesRule(selected_channel, rule))) {
        channelMatches = true;
      }
      if ($scope.show_sc && rule.scheduled_change !== null) {
        if (rule.scheduled_change.channel && $scope.channelMatchesRule(selected_channel, rule.scheduled_change) ||
            (rule.scheduled_change.change_type !== "delete" && !rule.scheduled_change.channel)) {
          channelMatches = true;
        }
      }
      return productMatches && channelMatches;
    }
    else {
      product = rule.product === $scope.pr_ch_selected[0];
      return (product || !rule.product);
    }
  };

  $scope.filterScheduledChanges = function(rule) {
    if (! $scope.show_sc && rule.scheduled_change !== null && rule.scheduled_change.change_type === "insert") {
      return false;
    }
    return true;
  };

  $scope.locationChanger = function () {
    changeLocationWithFilterParams($scope.pr_ch_filter);
  };


  $scope.openUpdateModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_modal.html',
      controller: 'RuleEditCtrl',
      size: 'lg',  // can be lg or sm
      backdrop: 'static',
      resolve: {
        // items: function () {
        //   return $scope.items;
        // },
        rule: function () {
          return rule;
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
        pr_ch_options: function() {
          return $scope.pr_ch_options;
        }
      }
    });
  };
  /* End openUpdateModal */

  $scope.openNewScheduledRuleModal = function() {

    // prepopulate the product and channel if the Rules have already been filtered by one.
    var product = "";
    var channel = "";
    if ($scope.pr_ch_selected[0].toLowerCase() !== "all rules") {
      product = $scope.pr_ch_selected[0];
      if ($scope.pr_ch_selected.length > 1) {
        channel = $scope.pr_ch_selected[1];
      }
    }

    var modalInstance = $modal.open({
      templateUrl: 'rule_scheduled_change_modal.html',
      controller: 'NewRuleScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          // blank new default rule
          return {
            base_row: undefined,
            product: product,
            channel: channel,
            backgroundRate: 0,
            priority: 0,
            update_type: 'minor',
            when: null,
            change_type: 'insert',
          };
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
      }
    });
    modalInstance.result.then(function(sc) {
      var rule = {"scheduled_change": sc};
      $scope.rules.push(rule);
    });
  };

  $scope.openNewScheduledRuleChangeModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_scheduled_change_modal.html',
      controller: 'NewRuleScheduledChangeCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          sc = angular.copy(rule);
          sc["change_type"] = "update";
          return sc;
        },
        original_row: function() {
          return rule;
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
      }
    });
    modalInstance.result.then(function(sc) {
      rule.scheduled_change = sc;
    });
  };

  $scope.openNewScheduledDeleteModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_scheduled_delete_modal.html',
      controller: 'NewRuleScheduledChangeCtrl',
      size: 'lg',
      resolve: {
        scheduled_changes: function() {
          return [];
        },
        sc: function() {
          return {
            "base_row": rule,
            "rule_id": rule.rule_id,
            "data_version": rule.data_version,
            "change_type": "delete"
          };
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
      }
    });
    modalInstance.result.then(function(sc) {
      rule.scheduled_change = sc;
    });
  };

  $scope.openEditScheduledRuleChangeModal = function(rule) {
    var modalInstance = $modal.open({
      templateUrl: 'rule_scheduled_change_modal.html',
      controller: "EditRuleScheduledChangeCtrl",
      size: 'lg',
      backdrop: 'static',
      resolve: {
        sc: function() {
          var sc = angular.copy(rule.scheduled_change);
          return sc;
        },
        original_row: function() {
          return rule;
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
        rule: function() {
          return rule;
        },
      }
    });
    modalInstance.result.then(function(action) {
      if (action === "delete") {
        rule.scheduled_change = null;
        if (!rule.rule_id) {
          $scope.rules = $scope.rules.filter(function(element) {
            if (!element.rule_id) {
              return false;
            }
            return true;
          });
        }
      }
    });
  };

  $scope.openDeleteModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_delete_modal.html',
      controller: 'RuleDeleteCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        rule: function () {
          return rule;
        },
        rules: function() {
          return $scope.rules;
        },
      }
    });
  };
  /* End openDeleteModal */

  $scope.openNewRuleModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'rule_modal.html',
      controller: 'NewRuleCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        rules: function() {
          return $scope.rules;
        },
        rule: function() {
          // blank new default rule
          return {
            product: '',
            backgroundRate: 0,
            priority: 0,
            update_type: 'minor',
            _duplicate: false,
          };
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
        pr_ch_options: function() {
          return $scope.pr_ch_options;
        }
      }
    });
  };
  /* End openNewRuleModal */

  $scope.openDuplicateModal = function(rule) {
    var modalInstance = $modal.open({
      templateUrl: 'rule_modal.html',
      controller: 'NewRuleCtrl',
      size: 'lg',
      backdrop: 'static',
      resolve: {
        rules: function() {
          return $scope.rules;
        },
        rule: function() {
          var copy = angular.copy(rule);
          delete copy.data_version;
          delete copy.rule_id;
          copy._duplicate = true;
          return copy;
        },
        signoffRequirements: function() {
          return $scope.signoffRequirements;
        },
        pr_ch_options: function() {
          return $scope.pr_ch_options;
        }
      }
    });
  };
  /* End openDuplicateRuleModal */

  $scope.openRevertModal = function(revision) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_revert_modal.html',
      controller: 'RuleRevertCtrl',
      backdrop: 'static',
      // size: 'sm',
      resolve: {
        revision: function () {
          return revision;
        }
      }
    });

    modalInstance.result.then(function () {
      // this will cause another fetch of rules
      // because it will start the RulesController
      $location.path('/rules');
    }, function () {
      // modal closed
    });
  };
  /* End openDeleteModal */

  $scope.openReleaseDataModal = function(mapping) {
    Releases.getRelease(mapping)
    .success(function(response) {
      // it's the same rule, but this works
      var modalInstance = $modal.open({
        templateUrl: 'release_data_modal.html',
        controller: 'ReleaseDataCtrl',
        size: 'lg',
        backdrop: 'static',
        resolve: {
          release: function () {
            return response;
          },
          diff: function() {
            return false;
          }
        }
      });
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  };
  /* End openDataModal */

  $scope.signoff = function(sc) {
    var modalInstance = $modal.open({
      templateUrl: "signoff_modal.html",
      controller: "SignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Rule";
        },
        service: function() {
          return Rules;
        },
        current_user: function() {
          return $scope.current_user;
        },
        user_roles: function() {
          return $scope.user_roles;
        },
        required_signoffs: function () {
          return sc["required_signoffs"];
        },
        sc: function() {
          return sc;
        },
        pk: function() {
          return {"rule_id": sc["rule_id"]};
        },
        // TODO: this should really show the diff.
        data: function() {
          return {
            "Product": sc["product"],
            "Channel": sc["channel"],
            "Mapping": sc["mapping"],
            "Priority": sc["priority"],
            "Background Rate": sc["backgroundRate"],
          };
        },
      }
    });
  };

  $scope.revokeSignoff = function(sc) {
    $modal.open({
      templateUrl: "revoke_signoff_modal.html",
      controller: "RevokeSignoffCtrl",
      backdrop: "static",
      resolve: {
        object_name: function() {
          return "Rule";
        },
        service: function() {
          return Rules;
        },
        current_user: function() {
          return $scope.current_user;
        },
        sc: function() {
          return sc;
        },
        pk: function() {
          // TODO: add alias here if it exists
          return {"rule_id": sc["rule_id"]};
        },
        // TODO: this should really show the diff.
        data: function() {
          return {
            "Product": sc["product"],
            "Channel": sc["channel"],
            "Mapping": sc["mapping"],
            "Priority": sc["priority"],
            "Background Rate": sc["backgroundRate"],
          };
        },
      }
    });
  };


});
