# TODO: Make this rely on things that are not straight-up exec.
class balrog {
    $db_name = $DB_NAME
    $db_user = $DB_USER
    $db_pass = $DB_PASS
    $db_ro_user = $DB_RO_USER
    $db_ro_pass = $DB_RO_PASS
    # create config files
    file {
        "/etc/aus":
            ensure => directory;
        "$PROJ_DIR/admin.ini":
            content => template("$PROJ_DIR/puppet/templates/admin.ini.erb"),
            backup => true;
        "$PROJ_DIR/balrog.ini":
            content => template("$PROJ_DIR/puppet/templates/balrog.ini.erb"),
            backup => true;
        "/var/log/aus.log":
            ensure => present,
            owner => apache,
            group => apache,
            mode => 644;
        "/var/log/ausadmin.log":
            ensure => present,
            owner => apache,
            group => apache,
            mode => 644;
        "/var/log/auscef.log":
            ensure => present,
            owner => apache,
            group => apache,
            mode => 644;
    }
    # import mysqldump
    exec { "create_mysql_database":
        command => "mysql -uroot -B -e'CREATE DATABASE $DB_NAME CHARACTER SET utf8;'",
        unless  => "mysql -uroot -B --skip-column-names -e 'show databases' | /bin/grep '$DB_NAME'",
    }

    exec { "grant_mysql_database":
        command => "mysql -uroot -B -e'GRANT ALL PRIVILEGES ON $DB_NAME.* TO $DB_USER@localhost IDENTIFIED BY \"$DB_PASS\"'",
        unless  => "mysql -uroot -B --skip-column-names mysql -e 'select user from user' | grep '$DB_USER'",
        require => Exec["create_mysql_database"];
    }

    exec { "create_tables":
        command => "python $PROJ_DIR/scripts/manage-db.py --db mysql://$DB_USER:$DB_PASS@localhost/$DB_NAME create",
        require => Exec["grant_mysql_database"];
    }

    exec { "grant_ro_mysql_database":
        command => "mysql -uroot -B -e'GRANT SELECT ON $DB_NAME.* TO $DB_RO_USER@localhost IDENTIFIED BY \"$DB_RO_PASS\"'",
        unless  => "mysql -uroot -B --skip-column-names mysql -e 'select user from user' | grep '$DB_RO_USER'",
        require => Exec["create_mysql_database"];
    }

    exec {"import_sample_data":
        command => "/bin/cat $PROJ_DIR/puppet/files/sample-data.sql | mysql -uroot -D $DB_NAME && touch /home/vagrant/import-done",
        unless => "test -f /home/vagrant/import-done",
        require => Exec["create_tables"];
    }
}
