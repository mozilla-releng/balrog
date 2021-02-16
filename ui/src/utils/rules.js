const ruleMatchesChannel = (rule, channel) => {
  // if neither the rule nor the scheduled rule's channel is an exact
  // match for the filter (after stripping away a possible wildcard)
  // this rule does not match
  // similarly, if the rule or scheduled rule has a wildcard, and the
  // selected channel does not match either, this rule does not match
  const ruleChannel = rule.channel;
  const scChannel =
    rule.scheduledChange && rule.scheduledChange.channel;
  let ruleChannelMatches = false;
  let scChannelMatches = false;

  if (ruleChannel) {
    if (ruleChannel.indexOf('*') === -1) {
      if (ruleChannel === channel) {
        ruleChannelMatches = true;
      }
    } else if (channel.startsWith(ruleChannel.split('*')[0])) {
      ruleChannelMatches = true;
    }
  } else {
      ruleChannelMatches = true;
    }

  if (scChannel) {
    if (scChannel.indexOf('*') === -1) {
      if (scChannel === channel) {
        scChannelMatches = true;
      }
    } else if (channel.startsWith(scChannel.split('*')[0])) {
      scChannelMatches = true;
    }
  } else {
      if (rule.scheduledChange) {
      scChannelMatches = true;
      }
  }

  if (ruleChannelMatches || scChannelMatches) {
    return true;
  }

  return false;
};

export {
  // eslint-disable-next-line import/prefer-default-export
  ruleMatchesChannel,
};
