/*global: sweetAlert */

angular.module("app").factory('errorSniffer', ['$q', function($q) {
  return {
    responseError: function(rejection) {
      if (rejection.status === 401) {
        // Unauthorized
        sweetAlert("Unauthorized", rejection.data, "error");
      } else if (rejection.status === 500) {
        sweetAlert(
          "Internal Server Error",
          "An unexpected server error happened. See the console log for more details.",
          "error"
        );
        console.warn(rejection.status, rejection.data);
      // } else {
      //   console.warn(rejection.status);
      }
      return $q.reject(rejection);
    }
  };
}]);

angular.module("app").config(['$httpProvider', function($httpProvider) {
    $httpProvider.interceptors.push('errorSniffer');
}]);


angular.module("app").controller('RulesController',
function($scope, $routeParams, $location, $timeout, RulesService, $modal) {

  $scope.rule_id = parseInt($routeParams.id, 10);
  if ($scope.rule_id) {
    // history of a specific rule
    RulesService.getHistory($scope.rule_id)
    .success(function(response) {
      // it's the same rule, but this works
      $scope.rules = response.rules;
    }).error(function() {
      console.error(arguments);
    });
  } else {
    RulesService.getRules()
    .success(function(response) {
      $scope.rules = response.rules;
    }).error(function() {
      console.error(arguments);
    });
  }

  if ($scope.rule_id) {
    $scope.ordering = ['-data_version'];
  } else {
    $scope.ordering = ['priority', 'version', 'mapping'];
  }


  $scope.currentPage = 1;
  $scope.pageSize = 10;  // default

  $scope.filters = {
    search: '',
  };

  $scope.date_thing = new Date();

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


  $scope.word_regexes = [];
  var keyword_regex = /\b(product|channel|mapping):\s*(\w+)/gi;
  $scope.$watchCollection('filters.search_actual', function(value) {
    $scope.word_regexes = [];
    if (value) {
      var matches;
      // var value="product: firefox b2g and channel: otherthing something";
      // console.log('Value:', value, word_regexes.length);
      while ((matches = keyword_regex.exec(value)) !== null) {
        // console.log(matches[0], matches[1], matches[2]);
        $scope.word_regexes.push(
          [new RegExp('\\b' + escapeRegExp(matches[2]), 'i'), matches[1], matches[0]]
        );
        // console.log('  matches:', matches);
      }
      value = value.replace(keyword_regex, '').trim();
      // console.log('leftover', value);
      // console.log('word_regexes1', word_regexes, word_regexes.length);
      // _.each(/\b(product|channel|mapping):\s*(\w+)/i.exec(value), function(match) {
      //   console.log("MATCH", match);
      // });
      _.each(value.trim().split(' '), function(term) {
        if (term.length) {
          $scope.word_regexes.push(
            [new RegExp('\\b' + escapeRegExp(term), 'i'), '*', term]
          );
        }
      });
      // console.log('word_regexes2', word_regexes, word_regexes.length);
    }
  });

  $scope.filterBySearch = function(rule) {
    // basically, look for a reason to NOT include this
    if ($scope.word_regexes.length) {
      // every word in the word_regexes array needs to have some match
      var matches = 0;
      _.each($scope.word_regexes, function(each) {
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
      });
      return matches === $scope.word_regexes.length;
    }

    return true;  // include it
  };

  // XXX this doesn't need to be in this controller
  $scope.splitFilterSearch = function(search) {
    var words = [];
    _.each(search.split(' '), function(term) {
      words.push(term.trim());
    });
    return words;
  };
  $scope.removeFilterSearchWord = function(word, search) {
    var regex = new RegExp('\\b' + escapeRegExp(word) + '\\b', 'i');
    return search.replace(regex, '').trim();
    // console.log('Remove', word, 'from', $scope.filters.search);
  };
  /* End filtering */

  /* Highlighting */
  $scope.highlightSearch = function(text, what) {
    if (!text) {
      return '';
    }
    if (text === null) {
      return text;
    }
    text = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    if (!$scope.word_regexes.length) {
      return text;
    }
    // `word_regexes` is a list of lists [regex, on what]
    _.each($scope.word_regexes, function(each) {
      var regex = each[0];
      var on = each[1];
      if (on === '*' || on === what) {
        _.each(regex.exec(text), function(match) {
          text = text.replace(match, '<span class="match">' + match + '</span>');
        });
      }
    });
    return text;
  };
  /* End highlighting */

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
      // $scope.selected = selectedItem;
      $location.path('/rules');
    }, function () {
      // console.log('modal closed');
    });
  };
  /* End openDeleteModal */

});
