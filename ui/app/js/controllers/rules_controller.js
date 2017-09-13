angular.module("app").controller('RulesController',
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route, Releases, Page) {

  Page.setTitle('Rules');

  $scope.loading = true;
  $scope.failed = false;

  $scope.rule_id = parseInt($routeParams.id, 10);
  $scope.pr_ch_options = [];

  $scope.currentPage = 1;
  $scope.pagesize_options = [10, 25, 50, 100]
  $scope.pageSize = $scope.pagesize_options[0];
  $scope.maxSize = 10;
  $scope.rules = [];
  $scope.pr_ch_filter = "";

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
              rule.scheduled_change = sc.change_type;
            }
          });
          $scope.rules.push(rule);
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
            $scope.pr_ch_filter = localStorage.getItem('pr_ch_filter');
          }
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

  $scope.$watch('ordering_str', function(value) {
    $scope.ordering = value.value.split(',');
  });

  $scope.$watch('pageSize', function(value) {
    $scope.pageSize = value;
  });

  $scope.$watch('pr_ch_filter', function(value) {
    if (value) {
      localStorage.setItem("pr_ch_filter", value);
    }
    $scope.pr_ch_selected = value.split(',');
  });

  if ($scope.rule_id) {
    $scope.ordering_options = [
      {
        text: "Data Version",
        value: "-data_version"
      },
    ];
  } else {
    $scope.ordering_options = [
      {
        text: "Priority, Version, Mapping",
        value: "-priority,version,mapping"
      },
      {
        text: "Product, Channel",
        value: "product,channel"
      },
      {
        text: "Mapping",
        value: "mapping"
      },
    ];
  }
  $scope.ordering_str = $scope.ordering_options[0];

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return !!(false || $scope.filters.search.length);
  };

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  $scope.$watchCollection('filters.search', function(value) {
    $location.hash(value);
    Search.noticeSearchChange(
      value,
      ['product', 'channel', 'mapping', 'comment']
    );
  });

  // I don't know how else to expose this to the templates
  $scope.getWordRegexes = Search.getWordRegexes;
  $scope.highlightSearch = Search.highlightSearch;
  $scope.removeFilterSearchWord = Search.removeFilterSearchWord;

  $scope.filterBySelect = function(rule) {
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
    modalInstance.result.then(function(change_type) {
      rule.scheduled_change = change_type;
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
    modalInstance.result.then(function(change_type) {
      rule.scheduled_change = change_type;
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


});
