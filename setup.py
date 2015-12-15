from setuptools import setup


setup(
    name="balrog",
    version="1.0",
    description="Mozilla's Update Server",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    packages=[
        "auslib",
        "auslib.admin",
        "auslib.admin.views",
        "auslib.blobs",
        "auslib.migrate",
        "auslib.migrate.versions",
        "auslib.util",
        "auslib.web",
        "auslib.web.views",
    ],
    include_package_data=True,
    install_requires=[
        "flask==0.10.1",
        "Werkzeug==0.11.2",
        "wtforms==2.1",
        "flask-wtf==0.12",
        "sqlalchemy-migrate==0.7.2",
        "tempita==0.5.1",
        "decorator==4.0.6",
        "blinker==1.4",
        "cef==0.5",
        "flask-compress==1.3.0",
        "itsdangerous==0.24",
        "repoze.lru==0.6",
    ],
    url="https://github.com/mozilla/balrog",
)
