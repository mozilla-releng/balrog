from setuptools import find_packages, setup


setup(
    name="balrog",
    version="1.0",
    description="Mozilla's Update Server",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    packages=find_packages(exclude=["vendor"]),
    include_package_data=True,
    install_requires=[
        "blinker==1.4",
        "cef==0.5",
        "decorator==4.0.6",
        "flask==0.10.1",
        "flask-compress==1.3.0",
        "flask-wtf==0.12",
        "itsdangerous==0.24",
        "jinja2==2.5.5",
        "jsonschema==2.5.1",
        "mysql-python==1.2.3",
        "pyyaml==3.11",
        "repoze.lru==0.6",
        "simplejson==2.0.9",
        "sqlalchemy==0.7.1",
        "sqlalchemy-migrate==0.7.2",
        "tempita==0.5.1",
        "uwsgi==2.0.11.2",
        "Werkzeug==0.11.2",
        "wtforms==2.1",
    ],
    url="https://github.com/mozilla/balrog",
)
