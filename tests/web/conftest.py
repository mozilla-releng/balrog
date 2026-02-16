import fakeredis
import pytest

from auslib.global_state import cache
from auslib.util.cache import TwoLayerCache
from auslib.web.public.base import create_app


@pytest.fixture(scope="class")
def app(request):
    redis = fakeredis.FakeRedis()
    cache.factory = lambda name, maxsize, timeout, redis_loads=None: TwoLayerCache(redis, name, maxsize, timeout, redis_loads)
    connexion_app = create_app()
    app = request.cls.app = connexion_app.app
    app.testing = True
    return app
