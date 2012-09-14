# Red Hat, CentOS, and Fedora think Apache is the only web server
# ever, so we have to use a different package on CentOS than Ubuntu.
class apache {
    file {
        "/var/log/httpd/aus4.mozilla.org":
            ensure => directory;
    }
    case $operatingsystem {
        centos: {
            package { "httpd-devel":
                ensure => present,
                before => File['/etc/httpd/conf.d/balrog.conf'];
            }

            file { "/etc/httpd/conf.d/balrog.conf":
                source => "$PROJ_DIR/puppet/files/etc/httpd/conf.d/balrog.conf",
                owner => "root", group => "root", mode => 0644,
                require => [
                    Package['httpd-devel']
                ];
            }

            service { "httpd":
                ensure => running,
                enable => true,
                require => [
                    Package['httpd-devel'],
                    File['/etc/httpd/conf.d/balrog.conf']
                ];
            }

        }
        ubuntu: {
            package { "apache2-dev":
                ensure => present,
                before => File['/etc/apache2/sites-enabled/balrog.conf'];
            }

            file { "/etc/apache2/sites-enabled/balrog.conf":
                source => "$PROJ_DIR/puppet/files/etc/httpd/conf.d/balrog.conf",
                owner => "root", group => "root", mode => 0644,
                require => [
                    Package['apache2-dev']
                ];
            }

	    exec {
	    	 'a2enmod rewrite':
		 	  onlyif => 'test ! -e /etc/apache2/mods-enabled/rewrite.load';
		 'a2enmod proxy':
		 	  onlyif => 'test ! -e /etc/apache2/mods-enabled/proxy.load';
	    }

            service { "apache2":
                ensure => running,
                enable => true,
                require => [
                    Package['apache2-dev'],
                    File['/etc/apache2/sites-enabled/balrog.conf']
                ];
            }

        }
    }
}
