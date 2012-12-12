import collections
import time
from flask import render_template, request
from auslib.admin.views.base import AdminView
from auslib.admin.base import db
from auslib.util import PrinterFriendlyDict
from auslib.util.timesince import timesince


class IndexPageView(AdminView):
    """/index.html"""
    def get(self):
        data = {
            'count_rules': db.rules.countRules(),
            'count_releases': db.releases.countReleases(),
            'count_users': db.permissions.countAllUsers(),
        }

        return render_template('index.html', **data)


class RecentChangesTableView(AdminView):
    """/recent_changes_table.html

    The reason for making this a view that returns just the <table> part
    without wrapping in <html> or anything is so we can extend it to fetch
    something like 10 more rows (where timestamp < latest last timestamp)
    without having to refresh the page or having to use a paginator.

    Also, by making the this table load async on the home page makes the
    home page snappy and load quicker.
    """

    history_keys = (
        'change_id', 'changed_by', 'timestamp', 'data_version'
    )

    @property
    def tables(self):
        return {
            'rule': db.rules,
            'permission': db.permissions,
            'release': db.releases,
        }

    def getAllRecentChanges(self, limit):
        for label, table in self.tables.items():
            rows = table.getRecentChanges(limit=limit)
            for row in rows:
                yield (label, row)

    def get(self):
        limit = int(request.args.get('limit', 10))

        # we select `limit` for each history table, now they need to battle
        # it out
        all = list(self.getAllRecentChanges(limit))

        # youngest first
        all.sort(lambda x, y: cmp(y[1]['timestamp'], x[1]['timestamp']))
        # the list is cut short (to the length of `limit`) by a break in
        # the loop
        changes = collections.defaultdict(dict)
        other_values = collections.defaultdict(dict)
        recent_changes = []
        for label, each in all:
            primary_keys = self.tables[label].history.base_primary_key
            values = [each[x] for x in primary_keys]
            other_values[label][each['change_id']] = dict(
                (x, each[x])
                for x in each
                if x not in primary_keys
            )
            changes[label][each['change_id']] = values

            if len(recent_changes) >= limit:
                # make sure this happens *after* `changes` is populated with
                # the "next" change
                break

            if each['data_version'] > 1:
                # easy, it's an update
                change = 'update'
            elif each['data_version'] == 1:
                # easy, it's an insert
                change = 'insert'
            else:
                # if the previous change_id had the same values for primary
                # keys then this was a deletion
                try:
                    previous_values = changes[label][each['change_id'] + 1]
                    if previous_values == values:
                        # it was one of those initial creation rows
                        continue
                    else:
                        change = 'delete'

                except KeyError:
                    # happens if this is the very latest change
                    change = 'delete'

            each['change'] = change
            # set a fancy `time_ago' field for human consumption
            each['time_ago'] = getTimeAgo(each['timestamp'])
            recent_changes.append((label, each))

        data = {
            'recent_changes': recent_changes,
        }
        data.update(
            self.decorateChanges(recent_changes, changes, other_values)
        )
        return render_template('fragments/recent_changes_table.html', **data)

    def decorateChanges(self, recent_changes, changes, other_values):
        """return a dict of dicts more verbose structures describing
        the deletes, updates and inserts.
        """
        diffs = collections.defaultdict(dict)
        deletes = collections.defaultdict(dict)
        inserts = collections.defaultdict(dict)

        for label, each in recent_changes:
            change_id = each['change_id']
            table = self.tables[label]
            primary_keys = table.history.base_primary_key

            if each['change'] in ('update', 'delete'):
                # we need the previous other values
                try:
                    # being able to look at the "next" change from the loop
                    # above is an early optimization.
                    # If "this" is the last element, then (last + 1) won't
                    # exist in `other_values` so...
                    prev_other_values = other_values[label][change_id - 1]
                except KeyError:
                    # ...we need to do another lookup just to fetch this data.
                    prev_change = table.history.getPrevChange(
                        change_id,
                        changes[label][change_id]
                    )
                    prev_other_values = dict(
                        (x, prev_change[x])
                        for x in prev_change
                        if x not in primary_keys
                    )

            if each['change'] == 'update':
                diffs[label][change_id] = PrinterFriendlyDict(
                    (k, (prev_other_values[k], value))
                    for k, value in other_values[label][change_id].items()
                    if k not in self.history_keys
                )

            elif each['change'] == 'delete':
                deletes[label][change_id] = PrinterFriendlyDict(
                    (k, changes[label][change_id][i])
                    for i, k in enumerate(primary_keys)
                )
                deletes[label][change_id].update(PrinterFriendlyDict(
                    (k, prev_other_values[k])
                    for k in prev_other_values
                    if k not in self.history_keys
                ))

            elif each['change'] == 'insert':
                inserts[label][change_id] = PrinterFriendlyDict(
                    (k, each[k])
                    for k in each
                    if k not in self.history_keys
                )

        return {
            'inserts': inserts,
            'deletes': deletes,
            'diffs': diffs,
        }


def getTimeAgo(timestamp):
    # keeping this here amongst the view code because the use of the
    # timesince() function is specific to the view
    now, then = int(time.time()), int(timestamp / 1000.0)
    time_ago = timesince(
        then,
        now,
        afterword='ago',
        minute_granularity=True
    )
    if not time_ago:
        time_ago = 'seconds ago'
    return time_ago
