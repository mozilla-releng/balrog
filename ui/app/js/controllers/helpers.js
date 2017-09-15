function isEmpty(obj) {
  if (obj === null || obj === undefined) {
    return true;
  }
  return Object.keys(obj).length === 0;
}

function fieldIsChanging(rule, fieldname) {
  return rule.scheduled_change !== null && rule[fieldname] !== rule.scheduled_change[fieldname];
}
