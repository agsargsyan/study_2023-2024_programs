from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.link import TCLink  
from mininet.cli import CLI
import time

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, num_hosts_r1, num_hosts_r2, **_opts):
        # Add 2 routers in two different subnets
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.1.0.1/24')


        # Adding hosts and specifying the default route dynamically
        for h in range(num_hosts_r1):
            host = self.addHost(name='h1{}'.format(h+1),
                                ip='10.0.0.{}/24'.format(h+251),
                                defaultRoute='via 10.0.0.1')
            self.addLink(host, r1, intfName2='r1-eth{}'.format(h+1), params2={'ip': '10.0.0.1/24'}, delay='5ms')

        for h in range(num_hosts_r2):
            host = self.addHost(name='h2{}'.format(h+1),
                                ip='10.1.0.{}/24'.format(h+252),
                                defaultRoute='via 10.1.0.1')
            self.addLink(host, r2, intfName2='r2-eth{}'.format(h+1), params2={'ip': '10.1.0.1/24'}, delay='2ms')

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth{}'.format(num_hosts_r1+1), intfName2='r2-eth{}'.format(num_hosts_r2+1),
                     params1={'ip': '10.100.0.1/24'}, params2={'ip': '10.100.0.2/24'})

def run(num_hosts_r1=2, num_hosts_r2=2):
    topo = NetworkTopo(num_hosts_r1=num_hosts_r1, num_hosts_r2=num_hosts_r2)
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth{}".format(num_hosts_r1+1)))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth{}".format(num_hosts_r2+1)))

    net.start()

    # Example of running network services and tests
    net.waitConnected()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run(2, 2)  

