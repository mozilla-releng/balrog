from connexion.middleware.main import ConnexionMiddleware, ServerErrorMiddleware


class BalrogServerErrorMiddleware(ServerErrorMiddleware):
    def __init__(self, next_app):
        # bypass ServerErrorMiddleware.__init__
        super(ServerErrorMiddleware, self).__init__(next_app, handler=self.error_response)


# Work around type incompatibility between connexion and starlette
# Replace ServerErrorMiddleware to set the handler so it can be async
middlewares = ConnexionMiddleware.default_middlewares.copy()
assert middlewares[0] is ServerErrorMiddleware
middlewares[0] = BalrogServerErrorMiddleware
