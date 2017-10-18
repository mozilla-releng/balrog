function isEmpty(obj) {
  if (obj === null || obj === undefined) {
    return true;
  }
  return Object.keys(obj).length === 0;
}

function fieldIsChanging(obj, fieldname) {
  return obj.scheduled_change !== null && obj[fieldname] !== obj.scheduled_change[fieldname];
}

function humanizeDate(when) {
  date = moment(when);
  return date.format('dddd, MMMM D, YYYY HH:mm:ss ') + 'GMT' + date.format('ZZ');
}

// We used to do this in a directive, but that didn't re-render when the value
// changed without a page reload, so we switched to this + ng-bind-html instead.
function formatMoment(when) {
  date = moment(when);
  return '<time title="' + humanizeDate(when) + '">' + date.fromNow() + '</time>';
}
