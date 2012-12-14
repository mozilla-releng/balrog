class PrinterFriendlyDict(dict):

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


def getPagination(page, total_count, page_size, max_range_length=10):
    max_ = total_count / page_size + 2
    min_ = 1
    naive_range = range(min_, max_)
    range_ = [page]
    i = 1
    max_range_length = min(max_range_length, len(naive_range))
    while len(range_) < max_range_length:
        left = page - i
        if left > 0:
            range_.insert(0, left)
        right = page + i
        if right in naive_range and len(range_) < max_range_length:
            range_.append(right)
        i += 1
    pagination = {
        'current_page': page,
        'range': range_
    }
    if (page - 1) * page_size > 0:
        pagination['prev'] = page - 1
    if page * page_size < total_count:
        pagination['next'] = page + 1
    return pagination
