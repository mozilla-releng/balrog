angular.module("app").factory('Search', function() {

  function escapeRegExp(string){
    return string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  var service = {
    word_regexes: []
  };

  service.getWordRegexes = function() {
    return service.word_regexes;
  };

  service.noticeSearchChange = function(value, keywords) {
    service.word_regexes = [];
    if (!value) {
      return;
    }
    // XXX this should be created from the @keywords argument
    var keyword_regex = /\b(product|channel|mapping):\s*(\w+)/gi;

    var matches;
    while ((matches = keyword_regex.exec(value)) !== null) {
      service.word_regexes.push(
        [new RegExp('\\b' + escapeRegExp(matches[2]), 'i'), matches[1], matches[0]]
      );
    }
    value = value.replace(keyword_regex, '').trim();
    _.each(value.trim().split(' '), function(term) {
      if (term.length) {
        service.word_regexes.push(
          [new RegExp('\\b' + escapeRegExp(term), 'i'), '*', term]
        );
      }
    });
  };

  service.highlightSearch = function(text, what) {
    if (!text) {
      return '';
    }
    if (text === null) {
      return text;
    }
    text = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    if (!service.word_regexes.length) {
      return text;
    }
    // `word_regexes` is a list of lists [regex, on what]
    _.each(service.word_regexes, function(each) {
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

  service.removeFilterSearchWord = function(word, search) {
    var regex = new RegExp('\\b' + escapeRegExp(word) + '\\b', 'i');
    return search.replace(regex, '').trim();
  };


  return service;

});
