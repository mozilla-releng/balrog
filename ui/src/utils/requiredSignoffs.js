const ruleMatchesRequiredSignoff = (rule, rs) => {
  if (rule.product && rule.product !== rs.product) {
    return false;
  }

  if (rule.channel && rule.channel !== rs.channel) {
    if (rule.channel.endsWith('*')) {
      // If a globbing rule's base doesn't match the required signoff channel
      // it doesn't apply
      if (rule.channel.substring(0, rule.channel.length - 1) !== rs.channel) {
        return false;
      }
    } else {
      // If there's no glob at all on the rule (and we've already determined
      // that it doesn't match the required signoff channel, it doesn't apply.
      return false;
    }
  }

  return true;
};

// Returns an object mapping each role to the number of signoffs required
// from it for the given rule. When multiple Required Signoffs match a rule
// (eg: a rule with no channel), the largest count for each role applies.
const getRequiredSignoffsForRule = (rule, requiredSignoffs) => {
  const result = {};

  requiredSignoffs.forEach((rs) => {
    if (ruleMatchesRequiredSignoff(rule, rs)) {
      result[rs.role] = Math.max(result[rs.role] || 0, rs.signoffs_required);
    }
  });

  return result;
};

export { getRequiredSignoffsForRule, ruleMatchesRequiredSignoff };
