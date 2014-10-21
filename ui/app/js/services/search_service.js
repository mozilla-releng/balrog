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
  return service;

});
