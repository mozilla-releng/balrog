angular.module("app").controller('RulesController',
function($scope, $routeParams, $location, $timeout, Rules, Search, $modal, $route) {

  // var lastRoute = $route.current;
  // if ($route.current.$route.templateUrl.indexOf('mycurrentpath') > 0) {
  //   $route.current = lastRoute;
  // }

  $scope.loading = true;
  $scope.failed = false;

  $scope.rule_id = parseInt($routeParams.id, 10);
  if ($scope.rule_id) {
    // history of a specific rule
    Rules.getHistory($scope.rule_id)
    .success(function(response) {
      // it's the same rule, but this works
      $scope.rules = response.rules;
    })
    .error(function() {
      console.error(arguments);
      $scope.failed = true;
    })
    .finally(function() {
      $scope.loading = false;
    });
  } else {
    Rules.getRules()
    .success(function(response) {
      $scope.rules = response.rules;
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
        value: "priority,version,mapping"
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


  $scope.currentPage = 1;
  $scope.pageSize = 10;  // default

  $scope.filters = {
    search: $location.hash(),
  };

  $scope.hasFilter = function() {
    return false || $scope.filters.search.length;
  };

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  // We don't want to immediately start searching on every typed
  // little character. Instead, bunch them up and search after a
  // little 200ms pause.
  var filters_search_timeout = null;
  var filters_search_temp = '';
  $scope.$watchCollection('filters.search', function(value) {
    // break up every entered word into a word delimited regex
    if (filters_search_timeout) {
      $timeout.cancel(filters_search_timeout);
    }
    filters_search_temp = value;
    filters_search_timeout = $timeout(function() {
      $scope.filters.search_actual = filters_search_temp;
    }, 300);
  });

  $scope.$watchCollection('filters.search_actual', function(value) {
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

  $scope.filterBySearch = function(rule) {
    // basically, look for a reason to NOT include this
    if (Search.word_regexes.length) {
      // every word in the word_regexes array needs to have some match
      var matches = 0;
      _.each(Search.word_regexes, function(each) {
        var regex = each[0];
        var on = each[1];
        // console.log(regex, on);
        if ((on === '*' || on === 'product') && rule.product && rule.product.match(regex)) {
          matches++;
          return;
        }
        if ((on === '*' || on === 'channel') && rule.channel && rule.channel.match(regex)) {
          matches++;
          return;
        }
        if ((on === '*' || on === 'mapping') && rule.mapping && rule.mapping.match(regex)) {
          matches++;
          return;
        }
        if ((on === '*' || on === 'comment') && rule.comment && rule.comment.match(regex)) {
          matches++;
          return;
        }
      });
      return matches === Search.word_regexes.length;
    }

    return true;  // include it
  };
  /* End filtering */

  $scope.openUpdateModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_modal.html',
      controller: 'RuleEditCtrl',
      // size: size,  // can be lg or sm
      resolve: {
        // items: function () {
        //   return $scope.items;
        // },
        rule: function () {
          return rule;
        }
      }
    });
    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openUpdateModal */

  $scope.openDeleteModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_delete_modal.html',
      controller: 'RuleDeleteCtrl',
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

    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openDeleteModal */

  $scope.openNewRuleModal = function() {

    var modalInstance = $modal.open({
      templateUrl: 'rule_modal.html',
      controller: 'NewRuleCtrl',
      // size: 'sm',
      resolve: {
        rules: function() {
          return $scope.rules;
        },
      }
    });

    modalInstance.result.then(function () {
      // $scope.selected = selectedItem;
    }, function () {
      console.log('modal closed');
    });
  };
  /* End openNewRuleModal */

  $scope.openRevertModal = function(rule) {

    var modalInstance = $modal.open({
      templateUrl: 'rule_revert_modal.html',
      controller: 'RuleRevertCtrl',
      // size: 'sm',
      resolve: {
        rule: function () {
          return rule;
        }
      }
    });

    modalInstance.result.then(function () {
      $location.path('/rules');
    }, function () {
      // console.log('modal closed');
    });
  };
  /* End openDeleteModal */

});
