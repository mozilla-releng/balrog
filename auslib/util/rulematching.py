import logging
import re

from auslib.util.comparison import int_compare, string_compare, version_compare


def matchRegex(foo, bar):
    # Expand wildcards and use ^/$ to make sure we don't succeed on partial
    # matches. Eg, 3.6* matches 3.6, 3.6.1, 3.6b3, etc.
    # Channel length must be strictly greater than two
    # And globbing is allowed at the end of channel-name only
    if foo.endswith('*'):
        if(len(foo) >= 3):
            test = foo.replace('.', r'\.').replace('*', r'\*', foo.count('*') - 1)
            test = '^{}.*$'.format(test[:-1])
            if re.match(test, bar):
                return True
            return False
        else:
            return False
    elif (foo == bar):
        return True
    else:
        return False


def matchCsv(csvString, queryString, substring=True):
    """Decides whether a column from a rule matches an incoming one.
       Some columns in a rule may specify multiple values delimited by a
       comma. Once split we do a full or substring match against the query
       string. Because we support substring matches, there's no need
       to support globbing as well."""
    if csvString is None:
        return True
    for part in csvString.split(','):
        if substring and part in queryString:
            return True
        elif part == queryString:
            return True
    return False


def matchSimpleExpressionSubRule(subRuleString, queryString, substring):
    """Performs the actual logical 'AND' operation on a rule as well as partial/full string matching
       for each section of a rule.
       If all parts of the subRuleString match the queryString, then we have successfully resolved the
       logical 'AND' operation and return True.
       Partial matching makes use of Python's "<substring> in <string>" functionality, giving us the ability
       for an incoming rule to match only a substring of a rule.
       Full matching makes use of Python's "<string> in <list>" functionality, giving us the ability for
       an incoming rule to exactly match the whole rule. Currently, incoming rules are comma-separated strings."""
    for rule in subRuleString:
        if substring and rule not in queryString:
            return False
        elif not substring and rule not in queryString.split(','):
            return False
    return True


def matchSimpleExpression(ruleString, queryString, substring=True):
    """Decides whether a column from a rule matches an incoming one using simplified boolean logic.
       Only two operators are supported: '&&' (and), ',' (or). A rule like 'AMD,SSE' will match incoming
       rules that contain either 'AMD' or 'SSE'. A rule like 'AMD&&SSE' will only match incoming rules
       that contain both 'AMD' and 'SSE'.
       This function can do substring matching or full string matching. When doing substring matching, a rule
       specifying 'AMD,Windows 10' WILL match an incoming rule such as 'Windows 10.1.2'. When doing full string
       matching, a rule specifying 'AMD,SSE' will NOT match an incoming rule that contains 'SSE3', but WILL match
       an incoming rule that contains either 'AMD' or 'SSE3'."""
    if ruleString is None:
        return True

    decomposedRules = [[rule.strip() for rule in subRule.split('&&')] for subRule in ruleString.split(',')]

    for subRule in decomposedRules:
        if matchSimpleExpressionSubRule(subRule, queryString, substring):
            # We can immediately return True on the first match because this loop is iterating over an OR expression
            # so we need just one match to pass.
            return True
    return False


def matchChannel(ruleChannel, queryChannel, fallbackChannel):
    """Decides whether a channel from the rules matches an incoming one.
       If the ruleChannel is null, we match any queryChannel. We also match
       if the channels match exactly, or match after wildcards in ruleChannel
       are resolved. Channels may have a fallback specified, too, so we must
       check if the fallback version of the queryChannel matches the ruleChannel."""
    if ruleChannel is None:
        return True
    if matchRegex(ruleChannel, queryChannel):
        return True
    if matchRegex(ruleChannel, fallbackChannel):
        return True


def matchVersion(ruleVersion, queryVersion):
    """Decides whether a version from the rules matches an incoming version.
       If the ruleVersion is null, we match any queryVersion. If it's not
       null, we must either match exactly, or match a comparison operator."""
    logging.debug('ruleVersion: %s, queryVersion: %s', ruleVersion, queryVersion)
    if ruleVersion is None:
        return True
    rulesVersionList = ruleVersion.split(",")
    for rule in rulesVersionList:
        if version_compare(queryVersion, rule):
            return True
    return False


def matchLocale(ruleLocales, queryLocale):
    """Decides if a comma seperated list of locales in a rule matches an
    update request"""
    return matchCsv(ruleLocales, queryLocale, substring=False)


def matchBuildID(ruleBuildID, queryBuildID):
    """Decides whether a buildID from the rules matches an incoming one.
       If the ruleBuildID is null, we match any queryBuildID. If it's not
       null, we must either match exactly, or match with a camparison
       operator."""
    if ruleBuildID is None:
        return True
    return string_compare(queryBuildID, ruleBuildID)


def matchMemory(ruleMemory, queryMemory):
    """Decides whether a memory value from the rules matches an incoming one.
       If the ruleMemory is null, we match any queryMemory. If it's not
       null, we must either match exactly, or match with a camparison
       operator."""
    if ruleMemory is None:
        return True
    return int_compare(queryMemory, ruleMemory)


def matchBoolean(ruleValue, queryValue):
    """As with all other columns, if the value isn't present in the Rule, the Rule matches.
    Unlike other columns, the non-existence of a boolean field in the updateQuery evaluates
    to False, so we need to handle True, False, and None explicitly. Note that None in the
    updateQuery is treated as "unknown", and will cause any Rule without an explicit value
    for the field to match.
    The full truth table is:
    rule | query | matches?
        F      0        Y
        F      1        N
        F     null      N
        T      0        N
        T      1        Y
        T     null      N
    null     0        Y
    null     1        Y
    null    null      Y

    Additional context in https://bugzilla.mozilla.org/show_bug.cgi?id=1386756"""

    if ruleValue is not None:
        if queryValue is None or ruleValue != queryValue:
            return False
    return True
