describe("Service: Search", function() {

  beforeEach(function() {
    module("app");
  });

  it('should start with now word regexes', inject(['Search',
  function(Search) {
    expect(Search.getWordRegexes()).toEqual([]);
  }]));

  it('should notice search changes', inject(['Search',
  function(Search) {
    Search.noticeSearchChange('peter', ['name', 'age']);
    expect(Search.getWordRegexes().length).toEqual(1);
    // we should be able to use one of those to match something
    var regex_group = Search.getWordRegexes()[0];
    expect(regex_group.length).toEqual(3);
    var regex = regex_group[0];
    var field = regex_group[1];
    var term = regex_group[2];
    expect(regex.test('Peter was here')).toEqual(true);
    expect(field).toEqual('*');
    expect(term).toEqual('peter');
  }]));

  it('should trim on whitespaces', inject(['Search',
  function(Search) {
    Search.noticeSearchChange('  peter  be ', []);
    expect(Search.getWordRegexes().length).toEqual(2);
    // we should be able to use one of those to match something
    var first = Search.getWordRegexes()[0];
    expect(first[2]).toEqual('peter');
    var second = Search.getWordRegexes()[1];
    expect(second[2]).toEqual('be');
  }]));

  it('should add no regexes if empty search', inject(['Search',
  function(Search) {
    Search.noticeSearchChange('   ', []);
    expect(Search.getWordRegexes().length).toEqual(0);
  }]));

  it('should notice search changes with keywords', inject(['Search',
  function(Search) {
    Search.noticeSearchChange('Name: Peter', ['name', 'age']);
    expect(Search.getWordRegexes().length).toEqual(1);
    // we should be able to use one of those to match something
    var regex_group = Search.getWordRegexes()[0];
    expect(regex_group.length).toEqual(3);
    var regex = regex_group[0];
    var field = regex_group[1];
    var term = regex_group[2];
    expect(regex.test('PETER was here')).toEqual(true);
    expect(field).toEqual('Name');
    expect(term).toEqual('Name: Peter');
  }]));


  it('should notice search changes multiple regexes', inject(['Search',
  function(Search) {
    Search.noticeSearchChange('name:peter be', ['name', 'age']);
    expect(Search.getWordRegexes().length).toEqual(2);
    // we should be able to use one of those to match something
    var regex_group = Search.getWordRegexes()[0];
    expect(regex_group.length).toEqual(3);
    var regex = regex_group[0];
    var field = regex_group[1];
    var term = regex_group[2];
    expect(regex.test('Some PETER thing')).toEqual(true);
    expect(regex.test('Salpeter is a chemical')).toEqual(false);
    expect(field).toEqual('name');

    regex_group = Search.getWordRegexes()[1];
    expect(regex_group.length).toEqual(3);
    regex = regex_group[0];
    field = regex_group[1];
    term = regex_group[2];
    expect(regex.test('you have to believe')).toEqual(true);
    expect(regex.test('Some PETER thing')).toEqual(false);
    expect(regex.test('Salpeter is a chemical')).toEqual(false);
    expect(field).toEqual('*');

  }]));

  it('should highlight simple words', inject(['Search',
  function(Search) {
    var func = Search.highlightSearch;
    // if the text is undefined, return ''
    expect(func(undefined)).toEqual('');
    // if it's null, return ''
    expect(func(null)).toEqual('');
    // all HTML should be escaped
    expect(func('<script>')).toEqual('&lt;script&gt;');

    // first notice a change
    Search.noticeSearchChange('peter script', ['name', 'age']);
    expect(func('PETER')).toEqual('<span class="match">PETER</span>');
    expect(func('<scripT>'))
    .toEqual('&lt;<span class="match">scripT</span>&gt;');
    expect(func('Peter Bengt'))
    .toEqual('<span class="match">Peter</span> Bengt');
    expect(func('Peterson Scriptson'))
    .toEqual('<span class="match">Peter</span>son ' +
             '<span class="match">Script</span>son');

  }]));

  it('should remove filer searches', inject(['Search',
  function(Search) {
    var func = Search.removeFilterSearchWord;
    expect(func('peter', 'peter be')).toEqual('be');
    // case insensitive
    expect(func('pEtEr', 'PeTeR be')).toEqual('be');
    // or nothing removed if not matched
    expect(func('peterbe', 'peter be')).toEqual('peter be');
    expect(func('peter', 'peterbe')).toEqual('peterbe');

  }]));

});
