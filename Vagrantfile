# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  config.vm.usable_port_range=(4000..9000)



  config.vm.define "jcv-backend" do |backend|
    backend.vm.hostname = "jcv-backend"
    backend.vm.network "public_network", type: "dhcp", bridge: "wlan0"
    backend.vm.network "forwarded_port", guest: 8000, host: 8000

    config.vm.provision "ansible" do |ansible|
      ansible.verbose = "v"
      ansible.playbook = "backend.yml"
    end

    backend.vm.post_up_message = "backend is ready"
    backend.vm.graceful_halt_timeout = 30

    backend.vm.provider "virtualbox" do |vbox|
      vbox.customize ["modifyvm", :id, "--cpuexecutioncap", "75" ]
      vbox.memory = 2048
      vbox.cpus = 2
    end
  end

  config.vm.define "jcv-frontend" do |front|
    front.vm.hostname = "jcv-frontend"
    front.vm.network "public_network", type: "dhcp", bridge: "wlan0"
    front.vm.network "forwarded_port", guest: 9000, host: 8500

    front.vm.graceful_halt_timeout = 30
    front.vm.post_up_message = "frontend is ready"

    front.vm.provider "virtualbox" do |vbox|
      vbox.memory = 1024
      vbox.cpus = 1
    end

    config.vm.provision "ansible" do |ansible|
      ansible.verbose = "v"
      ansible.playbook = "frontend.yml"
    end
  end
end
