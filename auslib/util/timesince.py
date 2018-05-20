from six import integer_types


# Language constants
MINUTE = 'minute'
MINUTES = 'minutes'
HOUR = 'hour'
HOURS = 'hours'
YEAR = 'year'
YEARS = 'years'
MONTH = 'month'
MONTHS = 'months'
WEEK = 'week'
WEEKS = 'weeks'
DAY = 'day'
DAYS = 'days'
AND = 'and'


def timesince(firstdate, seconddate,
              afterword=None,
              minute_granularity=False,
              max_no_sections=3,
              ):

    def wrap_afterword(result, afterword=afterword):
        if afterword is not None:
            return "%s %s" % (result, afterword)
        else:
            return result

    if (
        isinstance(firstdate, (int, integer_types)) and
        isinstance(seconddate, (int, integer_types))
    ):
        # two timestamps
        seconds = seconddate - firstdate
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        months = days / 30  # not accurate but ok
        years = months / 12
    else:
        difference = abs(seconddate - firstdate)
        day_difference = difference.days

        minutes = difference.seconds / 60
        hours = difference.seconds / 3600
        years = day_difference / 365
        months = (day_difference % 365) / 30
        days = (day_difference % 365) % 30
        minutes = ((day_difference % 365) % 30) % 24

    if days == 0 and months == 0 and years == 0:
        # use hours
        if hours == 1:
            return wrap_afterword("1 %s" % (HOUR))
        elif hours > 0:
            return wrap_afterword("%s %s" % (hours, HOURS))
        elif minute_granularity:
            if minutes == 1:
                return wrap_afterword("1 %s" % MINUTE)
            elif minutes > 0:
                return wrap_afterword("%s %s" % (minutes, MINUTES))
            else:
                # if the differnce is smaller than 1 minute,
                # return 0.
                return 0
        else:
            # if the difference is smaller than 1 hour,
            # return it false
            return 0
    else:
        s = []
        if years == 1:
            s.append('1 %s' % (YEAR))
        elif years > 1:
            s.append('%s %s' % (years, YEARS))

        if months == 1:
            s.append('1 %s' % MONTH)
        elif months > 1:
            s.append('%s %s' % (months, MONTHS))

        if days == 1:
            s.append('1 %s' % DAY)
        elif days == 7:
            s.append('1 %s' % WEEK)
        elif days == 14:
            s.append('2 %s' % WEEKS)
        elif days == 21:
            s.append('3 %s' % WEEKS)
        elif days > 14:
            weeks = days / 7
            days = days % 7
            if weeks == 1:
                s.append('1 %s' % WEEK)
            else:
                s.append('%s %s' % (weeks, WEEKS))
            if days % 7 == 1:
                s.append('1 %s' % DAY)
            elif days > 0:

                s.append('%s %s' % (days % 7, DAYS))
        elif days > 1:
            s.append('%s %s' % (days, DAYS))

        s = s[:max_no_sections]

        if len(s) > 1:
            return wrap_afterword("%s" % (' %s ' % AND).join(s))
        else:
            return wrap_afterword("%s" % s[0])
