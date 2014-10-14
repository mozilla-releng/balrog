angular.module("app").controller('RulesController',
function($scope, $location, $timeout, RulesService, $modal) {

  $scope.ordering = ['priority', 'version', 'mapping'];

  $scope.currentPage = 1;
  $scope.pageSize = 10;  // default

  $scope.filters = {
    search: '',
  };

  RulesService.getRules()
  .success(function(data) {
    $scope.rules = data.rules;
    $scope.total_count = data.count;
  }).error(function() {
    console.error(arguments);
  });

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
    }, 200);
  });

  var word_regexes = [];
  $scope.$watchCollection('filters.search_actual', function(value) {
    word_regexes = [];
    if (value) {
      _.each(value.split(' '), function(term) {
        word_regexes.push(
          new RegExp('\\b' + escapeRegExp(term), 'i')
        );
      });
    }
  });

  $scope.filterBySearch = function(rule) {
    // basically, look for a reason to NOT include this
    if (word_regexes.length) {
      // every word in the word_regexes array needs to have some match
      var matches = 0;
      _.each(word_regexes, function(regex) {
        if (rule.product && rule.product.match(regex)) {
          matches++;
          return;
        }
        if (rule.channel && rule.channel.match(regex)) {
          matches++;
          return;
        }
        if (rule.mapping && rule.mapping.match(regex)) {
          matches++;
          return;
        }
      });
      return matches === word_regexes.length;
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


  // $scope.credentials = { username: "", password: "" };
  //
  // var onLoginSuccess = function() {
  //   $location.path('/home');
  // };
  //
  // $scope.login = function() {
  //   AuthenticationService.login($scope.credentials).success(onLoginSuccess);
  // };
});


angular.module('app').controller('RuleEditCtrl',
function ($scope, $modalInstance, GeneralService, RulesService, rule) {

  $scope.original_rule = rule;
  $scope.rule = angular.copy(rule);

  $scope.saving = false;

  $scope.saveChanges = function () {
    $scope.saving = true;

    GeneralService.getCSRFToken()
    .success(function(r, s, headers) {
      var csrf_token = headers('X-CSRF-Token');
      RulesService.updateRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        // console.log('RESPONSE', response);
        $scope.rule.data_version = response.new_data_version;
        angular.copy($scope.rule, $scope.original_rule);
        $scope.saving = false;
        $modalInstance.close();
      }).error(function() {
        console.error(arguments);
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

angular.module('app').controller('RuleDeleteCtrl',
function ($scope, $modalInstance, GeneralService, RulesService, rule, rules) {

  //$scope.original_rule = rule;
  $scope.rule = rule;
  $scope.rules = rules;
  $scope.saving = false;
  // $scope.items = items;
  // $scope.selected = {
  //   item: $scope.items[0]
  // };

  $scope.saveChanges = function () {
    $scope.saving = true;
    GeneralService.getCSRFToken()
    .success(function(r, s, headers) {
      var csrf_token = headers('X-CSRF-Token');
      RulesService.deleteRule($scope.rule.id, $scope.rule, csrf_token)
      .success(function(response) {
        // console.log('RESPONSE', response);
        // $scope.rule.data_version = response.new_data_version;
        // angular.copy($scope.rule, $scope.original_rule);
        $scope.rules.splice($scope.rules.indexOf($scope.rule), 1);
        $scope.saving = false;
        $modalInstance.close();
      }).error(function() {
        console.error(arguments);
      });
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
