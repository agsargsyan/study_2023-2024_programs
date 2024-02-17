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
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.2.0.1/24')

        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1', ip='10.0.0.251/24', defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2', ip='10.2.0.251/24', defaultRoute='via 10.2.0.1')
        
        # Adding new hosts h3 and h4
        h3 = self.addHost(name='h3', ip='10.0.0.252/24', defaultRoute='via 10.0.0.1')
        h4 = self.addHost(name='h4', ip='10.2.0.252/24', defaultRoute='via 10.2.0.1')

        # Add host-router links for h1, h2, h3, and h4
        self.addLink(h1, r1, intfName2='r1-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(h2, r2, intfName2='r2-eth1', params2={'ip': '10.2.0.1/24'})
        self.addLink(h3, r1, intfName2='r1-eth3', params2={'ip': '10.0.0.1/24'})
        self.addLink(h4, r2, intfName2='r2-eth3', params2={'ip': '10.2.0.1/24'})

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.100.0.1/24'}, params2={'ip': '10.100.0.2/24'})

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.0.2 dev r1-eth2"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth2"))

    # Add red queue on r1-eth2 and r2-eth2
    net['r1'].cmd("tc qdisc add dev r1-eth2 root handle 1: prio")
    net['r1'].cmd("tc qdisc add dev r1-eth2 parent 1:1 handle 10: red limit 30000 min 2500 max 7500 avpkt 500 probability 0.1")

    net.start()
    net.waitConnected()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

