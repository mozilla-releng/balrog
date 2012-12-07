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
