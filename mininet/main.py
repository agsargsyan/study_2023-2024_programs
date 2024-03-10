from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from threading import Thread
import threading
import time

#класс для создание маршрутизаторов
class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

#создание топологии для сети
class NetworkTopo(Topo):
    def build(self, num_hosts_subnets, **_opts):
        #создание маршрутизаторы
        r0 = self.addHost('r0', cls=LinuxRouter, ip='10.0.0.1/24')
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.1.0.1/24')
        #добавление коммутаторов для связи хостов 
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        #соединение между маршрутизаторами и коммутаторами
        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '10.0.0.1/24'}, max_queue_size=300)
        self.addLink(s2, r1, intfName2='r1-eth1', params2={'ip': '10.1.0.1/24'}, max_queue_size=300)
        #соединение между маршрутизаторами
        self.addLink(r0, r1, 
        		intfName1='r0-eth2', 
        		intfName2='r1-eth2',
        		max_queue_size=30000, 
        		params1={'ip': '10.100.0.1/24', 'bw': '20'}, 
        		params2={'ip': '10.100.0.2/24', 'bw': '15'}
        		)
        #добавление оконечных устройств
        for i in range(1, 2*num_hosts_subnets + 1):
            host_ip = '10.0.0.{}/24' if i % 2 == 1 else '10.1.0.{}/24'
            default_route = 'via 10.0.0.1' if i % 2 == 1 else 'via 10.1.0.1'
            host = self.addHost(name='h{}'.format(i),
                                ip=host_ip.format(250 - i),
                                defaultRoute=default_route)
            switch = s1 if i % 2 == 1 else s2
            self.addLink(host, switch, bw = '100m')
            
iperf_time = 101 

                   
#Функция для запуска iperf между парой хостов
def run_iperf(net, host1_name, host2_name):
    global iperf_time 
    h1 = net.get(host1_name)
    h2 = net.get(host2_name)
    # Запуск iperf сервера на втором хосте
    h2.cmd("iperf3 -s -D -1")
    time.sleep(5)
    # Запуск iperf клиента на первом хосте, соединяющегося со вторым хостом
    h1.cmd(f"mkdir -p output/{host1_name}_to_{host2_name}")
    h1.cmd(f'iperf3 -c {h2.IP()} -b 100m -l 1000 -t {iperf_time} -J > output/{host1_name}_to_{host2_name}/{host1_name}_to_{host2_name}_iperf3.json')
    h1.cmd(f"cd output/{host1_name}_to_{host2_name} && plot_iperf.sh {host1_name}_to_{host2_name}_iperf3.json")


def monitor_queue(net, interface="r0-eth2", interval=0.1, output_file='queue_monitor.txt'):
    t = threading.current_thread()
    with open(output_file, 'w') as file:
        while getattr(t, "do_run", True):
            result = net['r0'].cmd(f'tc -s qdisc show dev {interface}')
            print(result, file=file)
            time.sleep(interval)




def run(num_hosts_subnets=20):
    topo = NetworkTopo(num_hosts_subnets=20)
    net = Mininet(topo=topo)

    avpkt = 1000
    #настройка алгоритма RED и tc  
    limit = avpkt * 300
    min_ = avpkt * 75
    max_ = avpkt * 150
    probability = 0.1
    bandwidth = 20
    #burst = 125
    #настройка парметров tcp окна
    tcp_min = avpkt * 1
    tcp_curr = avpkt * 4
    tcp_max = avpkt * 32


    # Add routing for reaching networks that aren't directly connected
    info(net['r0'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r0-eth2"))
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r1-eth2"))
    #установка типа окна TCP и ее размера
    info(net['c0'].cmd("sudo sysctl -w net.ipv4.tcp_congestion_control=reno"))
    info(net['c0'].cmd(f"sudo sysctl -w net.ipv4.tcp_rmem='{tcp_min} {tcp_curr} {tcp_max}'"))
    info(net['c0'].cmd(f"sudo sysctl -w net.ipv4.tcp_wmem='{tcp_min} {tcp_curr} {tcp_max}'"))

    
   
    
    #установка задержек на соединениях с помощью netem
    for i in range(1, 2*num_hosts_subnets + 1):
     host = net.get(f'h{i}')  # Генерируем имя хоста на основе i
     if (i%2==1):
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 20ms")
     else:
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 15ms") 

    

    net['r0'].cmdPrint("tc qdisc add dev r0-eth2 root handle 1: red limit {} min {} max {} avpkt {} bandwidth {} probability {}".format(limit, min_, max_, avpkt, bandwidth, probability))

    net.start()

    # Запуск мониторинга в отдельном потоке
    monitor_thread = Thread(target=monitor_queue, args=(net,))
    monitor_thread.start()  # Запуск потока мониторинга

    threads = []
   
    # Запуск iperf в отдельных потоках
    for i in range(1, 2*num_hosts_subnets, 2):
        host1 = f'h{i}'
        host2 = f'h{i+1}'
        t = Thread(target=run_iperf, args=(net, host1, host2))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  # Ожидание завершения всех потоков iperf

    # Остановка мониторинга
    monitor_thread.do_run = False  # Сигнал потоку мониторинга остановиться
    monitor_thread.join()  # Ожидание завершения потока мониторинга

    net.stop()  # Остановка сети

if __name__ == '__main__':
    setLogLevel('info')
    run()
