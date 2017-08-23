angular.module("app").controller('RulesController',
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route, Releases, Page, Permissions) {

  Page.setTitle('Rules');

  $scope.loading = true;
  $scope.failed = false;

  $scope.rule_id = parseInt($routeParams.id, 10);
  $scope.pr_ch_options = [];

  $scope.currentPage = 1;
  $scope.pageSize = 20;
  $scope.maxSize = 10;
  $scope.rules = [];
  $scope.pr_ch_filter = "";
  $scope.show_sc = true;

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
          $scope.pr_ch_filter = localStorage.getItem('pr_ch_filter') || "All rules";
        });
      });
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  }

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

  $scope.$watch('pr_ch_filter', function(value) {
    if (value) {
      localStorage.setItem("pr_ch_filter", value);
    }
    $scope.pr_ch_selected = value.split(',');
  });

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };

  $scope.isEmpty = function(obj) {
    return Object.keys(obj).length === 0;
  };

  $scope.formatMoment = function(when) {
    date = moment(when);
    // This is copied from app/js/directives/moment_directive.js
    // We can't use that for this page, because it doesn't re-render when
    // values change.
    return '<time title="' + date.format('dddd, MMMM D, YYYY HH:mm:ss ') + 'GMT' + date.format('ZZ') + '">' + date.fromNow() + '</time>';
  };

  $scope.orderRules = function(rule) {
    if (rule.priority === null || rule.priority === undefined) {
        return rule.scheduled_change.priority * -1;
    }
    else {
        return rule.priority * -1;
    }
  };

  $scope.filterBySelect = function(rule) {
    // TODO: put this elesewhere
    if (! $scope.show_sc && rule.scheduled_change !== null && rule.scheduled_change.change_type === "insert") {
      return false;
    }

    // Always return all entries if "all rules" is the filter
    // or if $scope.rule_id is set (meaning we're on the history page).
    if ($scope.pr_ch_selected[0].toLowerCase() === "all rules" || $scope.rule_id) {
      return true;
    }
    else if ($scope.pr_ch_selected && $scope.pr_ch_selected.length > 1) {
      product = rule.product === $scope.pr_ch_selected[0];
      channel = rule.channel && rule.channel === $scope.pr_ch_selected[1];
      return (product || !rule.product) && (channel || !rule.channel || (rule.channel && rule.channel.indexOf("*") > -1 && $scope.pr_ch_selected[1].startsWith(rule.channel.split("*")[0])));
    }
    else {
      product = rule.product === $scope.pr_ch_selected[0];
      return (product || !rule.product);
    }
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
        pr_ch_options: function() {
          return $scope.pr_ch_options;
        }
      }
    });
  };
  /* End openUpdateModal */

  $scope.openNewScheduledRuleModal = function() {

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
            product: product,
            channel: channel,
            backgroundRate: 0,
            priority: 0,
            update_type: 'minor',
            when: null,
            change_type: 'insert',
          };
        }
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
        }
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
          sc = angular.copy(rule);
          sc["change_type"] = "delete";
          return sc;
        }
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
          return rule.scheduled_change;
        }
      }
    });
    modalInstance.result.then(function(action) {
      if (action === "delete") {
        rule.scheduled_change = null;
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
        // todo: add more stuff here
        data: function() {
          return {
            "product": sc["product"],
            "channel": sc["channel"],
            "priority": sc["priority"],
            "backgroundRate": sc["backgroundRate"],
            "version": sc["version"],
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
        data: function() {
          return {
            "product": sc["product"],
            "channel": sc["channel"],
            "priority": sc["priority"],
            "backgroundRate": sc["backgroundRate"],
            "version": sc["version"],
          };
        },
      }
    });
  };


});
