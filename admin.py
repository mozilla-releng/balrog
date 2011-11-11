from paste.auth.basic import AuthBasicHandler

from auslib.web.base import app, db

db.setDburi('sqlite:////tmp/bhearsum.db')
db.createTables()
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG'] = True

def auth(environ, username, password):
    return username == password
app.wsgi_app = AuthBasicHandler(app.wsgi_app, "Balrog standalone auth", auth)
app.run()
