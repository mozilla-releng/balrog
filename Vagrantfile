MOUNT_POINT = '/home/vagrant/project'

Vagrant::Config.run do |config|
    config.vm.box = "centos-netboot"
    config.vm.box_url = "http://dl.dropbox.com/u/9227672/CentOS-6.0-x86_64-netboot-4.1.6.box"

    # Increase vagrant's patience during hang-y CentOS bootup
    # see: https://github.com/jedi4ever/veewee/issues/14
    config.ssh.max_tries = 50
    config.ssh.timeout   = 300

    config.vm.share_folder("v-root", MOUNT_POINT, ".")

    config.vm.forward_port 80, 9000

    config.vm.provision :puppet do |puppet|
        puppet.manifests_path = "puppet/manifests"
        puppet.manifest_file  = "vagrant.pp"
    end
end

print "Balrog has two applications: the Firefox-facing one, and the Admin one.\n"
print "They are accessed through different virtualhosts.\n"
print "You must add the following entries to /etc/hosts to work with them:\n"
print "127.0.0.1 balrog-admin.mozilla.dev\n"
print "127.0.0.1 balrog.mozilla.dev\n"
print "Once you've done that, you can access them by those names on port 8000.\n\n"
