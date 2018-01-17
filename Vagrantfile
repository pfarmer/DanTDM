Vagrant.configure("2") do |config|

    config.vm.box = "geerlingguy/centos7"

    config.vm.network :private_network, ip: "10.251.0.10"
    config.vm.hostname = 'dantdm.localhost'

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end

    config.vm.synced_folder ".", "/vagrant", :nfs => true

end
