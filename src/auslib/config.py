import logging

try:
    from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
except ImportError:  # pragma: no cover
    from configparser import RawConfigParser, NoSectionError, NoOptionError


class AUSConfig(object):
    required_options = {"logging": ["logfile"], "database": ["dburi"]}
    # Originally, this was done with getattr(logging, level), but it seems bad
    # to look up, and possibly return, arbitrary keys from a config file so it
    # was replaced with this simple mapping.
    loglevels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
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
        return self.cfg.get("logging", "logfile")

    def getLogLevel(self):
        try:
            return self.loglevels[self.cfg.get("logging", "level")]
        # NoOptionError is raised when we can't find the level in the config.
        # KeyError is raised when we can't find it in the mapping.
        except (NoOptionError, KeyError):
            return logging.WARNING

    def getDburi(self):
        return self.cfg.get("database", "dburi")

    def getDomainWhitelist(self):
        # the config should have a format like this
        # domain_whitelist = download.mozilla.org:Firefox|Fennec|Thunderbird, ftp.mozilla.org:SystemAddons
        try:
            whitelist_config = dict()
            pref = self.cfg.get("site-specific", "domain_whitelist").split(", ")
            for domain_pref in pref:
                domain, products = domain_pref.split(":")
                products = products.split("|")
                whitelist_config[domain] = tuple(products)
            return whitelist_config
        except (NoSectionError, NoOptionError):
            return dict()

    def getCaches(self):
        caches = {}
        if self.cfg.has_section("caches"):
            for cache_name in self.cfg.options("caches"):
                size, timeout = self.cfg.get("caches", cache_name).split(",")
                caches[cache_name] = (int(size), int(timeout))

        return caches


class AdminConfig(AUSConfig):
    required_options = {
        "logging": ["logfile"],
        "database": ["dburi"],
        "app": ["secret_key"],
        "site-specific": ["page_title"],
    }

    def getSecretKey(self):
        return self.cfg.get("app", "secret_key")

    def getSystemAccounts(self):
        try:
            return tuple(
                a.strip() for a in self.cfg.get("site-specific", "system_accounts").split(",")
            )
        except (NoSectionError, NoOptionError):
            return ()

    def getPageTitle(self):
        return self.cfg.get("site-specific", "page_title")


class ClientConfig(AUSConfig):
    def getSpecialForceHosts(self):
        try:
            return tuple(
                a.strip() for a in self.cfg.get("site-specific", "specialforcehosts").split(",")
            )
        except (NoSectionError, NoOptionError):
            return None
