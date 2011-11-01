from ConfigParser import RawConfigParser

class AUSConfig(object):
    required_options = {
        'logging': ['logfile'],
        'database': ['dburi']
    }

    def __init__(self, filename):
        self.cfg = RawConfigParser()
        self.cfg.read(filename)

    def validate(self):
        errors = []
        for section, options in self.required_options.items():
            if not self.cfg.has_section(section):
                errors.append("Missing section '%s'" % section)
            for opt in options:
                if not self.cfg.has_option(section, opt):
                    errors.append("Missing option '%s' from section '%s'" % (opt, section))
        return errors

    def getLogfile(self):
        return self.cfg.get('logging', 'logfile')

    def getDburi(self):
        return self.cfg.get('database', 'dburi')
