import getIndexOfSubStr from './getIndexOfSubStr';

// test me in local dev too!
const ruleMatchesChannel = (rule, channel) => {
  // we support globs at the end of a channel only, hence
  // splitting and taking the first part
  const matchesGlob = (r, c) =>
    (r && r.includes('*') && c.startsWith(r.split('*')[0])) ||
    c.substring(0, getIndexOfSubStr(c, '-', 1)) === r ||
    `${c.substring(0, getIndexOfSubStr(c, '-', 1))}*` === r;
  const ruleChannelMatches =
    // empty or absent channel matches anything
    // however, a rule could also be non-existent
    // (if a scheduled change is an insert)
    // in this case, channel will be undefined, and we should _never_
    // match on that, otherwise non-existent rules would show up
    // on all filters.
    rule.channel === null ||
    rule.channel === '' ||
    rule.channel === channel ||
    matchesGlob(rule.channel, channel);
  // if a scheduled change does not exist at all
  // we never want this to match, otherwise all rules
  // without scheduled changes will always match any filter
  const scChannelMatches = rule.scheduledChange
    ? (rule.scheduledChange.channel === null ||
        rule.scheduledChange.channel === '' ||
        rule.scheduledChange.channel === channel) &&
      matchesGlob(rule.scheduledChange.channel, channel)
    : false;

  return ruleChannelMatches || scChannelMatches;
};

export {
  // eslint-disable-next-line import/prefer-default-export
  ruleMatchesChannel,
};
