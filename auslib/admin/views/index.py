import collections
import time
from flask import render_template
from auslib.admin.views.base import AdminView
from auslib.admin.base import db
from auslib.util.timesince import timesince


class IndexPageView(AdminView):
    """/index.html"""
    def get(self):
        data = {
            'count_rules': db.rules.countRules(),
            'count_releases': db.releases.countReleases(),
            'count_users': db.permissions.countAllUsers(),
        }
        limit = 10

        tables = {
            'rule': db.rules,
            'permission': db.permissions,
            'release': db.releases,
        }

        # we select `limit` for each history table, now they need to battle it out
        all = []
        for label, table in tables.items():
            rows = table.getRecentChanges(limit=limit)
            for row in rows:
                all.append((
                    label,
                    row
                ))
        # youngest first
        all.sort(lambda x, y: cmp(y[1]['timestamp'], x[1]['timestamp']))
        #all = all[:limit]
        changes = collections.defaultdict(dict)
        other_values = collections.defaultdict(dict)
        recent_changes = []
        needs_diff = collections.defaultdict(list)
        inserts = collections.defaultdict(dict)
        _history_keys = ('change_id', 'changed_by', 'timestamp', 'data_version')
        for label, each in all:
            primary_keys = tables[label].history.base_primary_key
            values = [each[x] for x in primary_keys]
            other_values[label][each['change_id']] = dict(
              (x, each[x])
              for x in each
              if x not in primary_keys
            )

            changes[label][each['change_id']] = values
            change = None
            if each['data_version'] > 1:
                # easy, it's an update
                change = 'update'
                needs_diff[label].append(each['change_id'])
            elif each['data_version'] == 1:
                # easy, it's an insert
                change = 'insert'
                inserts[label][each['change_id']] = PrinterFriendlyDict(
                    (k, each[k])
                    for k in each
                    if k not in _history_keys
                )
            else:
                assert change is None
                # if the previous change_id had the same values for primary keys
                # then this was a deletion
                try:
                    previous_values = changes[label][each['change_id'] + 1]
                    #print "COMPARE", each['change_id']
                    #print "\t", previous_values
                    #print "\t", values
                    if previous_values == values:
                        # it was one of those initial creation rows
                        continue
                    else:
                        change = 'delete'
                        #print each

                except KeyError:
                    change = 'delete'
#                print "WHAT ABOUT"
#                print each

            each['change'] = change

            # set a fancy `time_ago' field for human consumption
            now, then = int(time.time()), int(each['timestamp'] / 1000.0)
            each['time_ago'] = timesince(
                then,
                now,
                afterword='ago',
                minute_granularity=True
            )
            if not each['time_ago']:
                each['time_ago'] = 'seconds ago'

            recent_changes.append((label, each))
            if len(recent_changes) >= limit:
                break


        #print needs_diff
        diffs = collections.defaultdict(dict)
        for label, change_ids in needs_diff.items():
            for change_id in change_ids:
                #print "\t", changes[label][change_id]
                #print "\t", changes[label][change_id - 1]
                #print
                #print "\t", other_values[label][change_id]
                #print "\t", other_values[label][change_id - 1]
                #print
                diffs[label][change_id] = PrinterFriendlyDict(
                    (k, (other_values[label][change_id - 1][k], value))
                    for k, value in other_values[label][change_id].items()
                    if k not in _history_keys
                )
#        print inserts
        #print diffs
        data['inserts'] = PrinterFriendlyDict(inserts)
        #data['inserts'] ={}
        data['diffs'] = PrinterFriendlyDict(diffs)
#        print repr(data['diffs'])
#        print type(data['diffs'])
#        print data['diffs'].items()
        data['recent_changes'] = recent_changes

        return render_template('index.html', **data)


class PrinterFriendlyDict(dict):

    #def __init__(self, *args, **kwargs):
    #    super(PrinterFriendlyDict, self).__init__(*args, **kwargs)


    def keys(self):
        keys = super(PrinterFriendlyDict, self).keys()
        return sorted(keys)

    def items(self):
        tuples = []
        for key in self.keys():
            value = self[key]
            if isinstance(value, (list, tuple)):
                value = [unicode(v) for v in value]
            else:
                value = unicode(value)
            tuples.append((key, value))
        return tuples
