// test me in local dev too!
const ruleMatchesChannel = (rule, channel) => {
  // we support globs at the end of a channel only, hence
  // splitting and taking the first part
  const matchesGlob = (r, c) =>
    r && r.includes('*') && c.startsWith(r.split('*')[0]);
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
  // if a scheduled change is a deletion
  // we never want scheduled deletions to match any filter
  // because the scheduled change channel on deletions is null
  // and the rule channel is a truthy value that might not equal 'channel'
  const scChannelMatches = rule.scheduledChange
    ? (rule.channel && ruleChannelMatches && rule.scheduledChange.channel === null) ||
      rule.scheduledChange.channel === '' ||
      rule.scheduledChange.channel === channel ||
      matchesGlob(rule.scheduledChange.channel, channel)
    : false;

  return ruleChannelMatches || scChannelMatches;
};

export {
  // eslint-disable-next-line import/prefer-default-export
  ruleMatchesChannel,
};
