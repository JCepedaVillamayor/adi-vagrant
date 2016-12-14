# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"

  config.vm.network "public_network"

  config.vm.define "jcp_backend" do |backend|
    backend.vm.hostname = "jcp-backend"
    backend.vm.network "forwarded_port", guest: 80, host: 5000

    backend.vm.post_up_message = "backend is ready"
    backend.vm.graceful_halt_timeout = 30

    backend.vm.provider "virtualbox" do |vbox|
      vbox.memory = 2048
      vbox.cpus = 2
    end
  end

  config.vm.define "jcp_frontend" do |front|
    front.vm.hostname = "jcp-front"
    front.vm.network "forwarded_port", guest: 80, host: 6000
    front.vm.graceful_halt_timeout = 30

    front.vm.post_up_message = "frontend is ready"

    front.vm.provider "virtualbox" do |vbox|
      vbox.memory = 1024
      vbox.cpus = 1
    end
  end
end
