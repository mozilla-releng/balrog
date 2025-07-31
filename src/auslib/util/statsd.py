from contextlib import contextmanager

from flask import g


class MaybeStatsd:
    @contextmanager
    def timer(self, *args, **kwargs):
        if g:
            with g.statsd.timer(*args, **kwargs):
                yield
        else:
            yield

    def incr(self, *args, **kwargs):
        if g:
            return g.statsd.incr(*args, **kwargs)


statsd = MaybeStatsd()
