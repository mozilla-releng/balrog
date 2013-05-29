# Install python and compiled modules for project
class python {
    case $operatingsystem {
        centos: {
            package {
                ["python-devel", "python-libs", "python-setuptools", "mod_wsgi"]:
                    ensure => installed;
            }

            exec { "pip-install":
                command => "easy_install -U pip",
                creates => "/usr/local/bin/pip",
                require => Package["python-devel", "python-setuptools"]
            }

            exec { "pip-install-compiled":
                command => "pip install -r $PROJ_DIR/requirements/compiled.txt",
                require => Exec['pip-install']
            }
        }

        ubuntu: {
            package {
                ["python2.6-dev", "python2.6", "libapache2-mod-wsgi", "python-wsgi-intercept", "python-pip"]:
                    ensure => installed;
            }

            exec { "pip-install-compiled":
                command => "pip install -r $PROJ_DIR/requirements/compiled.txt",
                require => Package['python-pip']
            }
        }
    }
}
