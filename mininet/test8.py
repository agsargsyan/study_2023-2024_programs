from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
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
    def build(self, num_hosts_subnets, **_opts):
        # Add 2 routers in two different subnets
        r0 = self.addHost('r0', cls=LinuxRouter, ip='10.0.0.1/24')
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.1.0.1/24')
        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # Add host-switch links in the same subnet
        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s2, r1, intfName2='r1-eth1', params2={'ip': '10.1.0.1/24'})
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r0, r1, 
        		intfName1='r0-eth2', 
        		intfName2='r1-eth2', 
        		params1={'ip': '10.100.0.1/24', 'bw': '20', 'max_queue_size': '300'}, 
        		params2={'ip': '10.100.0.2/24', 'bw': '15', 'max_queue_size': '300'}
        		)
         # Dynamically adding hosts and linking them to routers based on even/odd numbering
        for i in range(1, 2*num_hosts_subnets + 1):
            host_ip = '10.0.0.{}/24' if i % 2 == 0 else '10.1.0.{}/24'
            default_route = 'via 10.0.0.1' if i % 2 == 0 else 'via 10.1.0.1'
            host = self.addHost(name='h{}'.format(i),
                                ip=host_ip.format(250 - i),
                                defaultRoute=default_route)
            switch = s1 if i % 2 == 0 else s2
            self.addLink(host, switch, bw = 100)
            
            
            
            
            
            
def run(num_hosts_subnets=20):
    topo = NetworkTopo(num_hosts_subnets=20)
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r0'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r0-eth2"))
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r1-eth2"))

    info(net['r1'].cmd("sudo sysctl -w net.ipv4.tcp_congestion_control=reno"))	

    for i in range(1, 2*num_hosts_subnets + 1):
	    host = net.get(f'h{i}')  # Генерируем имя хоста на основе i
	    if (i%2==1):
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 20ms")
	    else:
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 15ms") 

    # Add red queue on r0-eth2 and r1-eth2
    net['r0'].cmdPrint("tc qdisc add dev r0-eth2 root handle 1: red limit 150000 min 32500 max 75000 avpkt 500 probability 0.1")
    
    net.start()
    
    h2 = net.get('h2')
    h2.cmdPrint("iperf3 -s -D -1")
    
    net.waitConnected()          
    h1 = net.get('h1')
    h1.cmdPrint('iperf3 -c', h2.IP(),'-w 16K -t 26 -J > iperf3.json')  # Replace with the IP address of h2
             
    h1.cmdPrint( 'ping -c 50', h2.IP(), '| grep "time=" | awk \'{print $5, $7}\' | sed -e \'s/time=//g\' -e\'s/icmp_seq=//g\' > ping.dat' )
    #CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

