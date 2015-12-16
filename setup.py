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
        "flask==0.10.1",
        "Werkzeug==0.9.6",
        "wtforms==2.0.1",
        "flask-wtf==0.10.2",
        "sqlalchemy-migrate==0.7.2",
        "tempita==0.5.1",
        "decorator==3.3.3",
        "blinker==1.2",
        "cef==0.5",
        "flask-compress==1.0.2",
        "itsdangerous==0.24",
        "repoze.lru==0.6",
    ],
    url="https://github.com/mozilla/balrog",
)
