from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from threading import Thread
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
        self.addLink(s1, r0, intfName2='r0-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s2, r1, intfName2='r1-eth1', params2={'ip': '10.1.0.1/24'})
        #соединение между маршрутизаторами
        self.addLink(r0, r1, 
        		intfName1='r0-eth2', 
        		intfName2='r1-eth2', 
        		params1={'ip': '10.100.0.1/24', 'bw': '20', 'max_queue_size': '300'}, 
        		params2={'ip': '10.100.0.2/24', 'bw': '15', 'max_queue_size': '300'}
        		)
        #добавление оконечных устройств
        for i in range(1, 2*num_hosts_subnets + 1):
            host_ip = '10.0.0.{}/24' if i % 2 == 1 else '10.1.0.{}/24'
            default_route = 'via 10.0.0.1' if i % 2 == 1 else 'via 10.1.0.1'
            host = self.addHost(name='h{}'.format(i),
                                ip=host_ip.format(250 - i),
                                defaultRoute=default_route)
            switch = s1 if i % 2 == 1 else s2
            self.addLink(host, switch, bw = 100)
            
# Функция для мониторинга очереди
def monitor_queue(net, interface, interval=1, output_file='queue_monitor.log'):
    with open(output_file, 'w') as file:
        try:
            while True:
                result = net['r0'].cmd(f'tc -s qdisc show dev {interface}')
                print(result, file=file)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Мониторинг завершен")
 
             
#Функция для запуска iperf между парой хостов
def run_iperf(net, host1_name, host2_name):
    h1 = net.get(host1_name)
    h2 = net.get(host2_name)
    # Запуск iperf сервера на втором хосте
    h2.cmdPrint("iperf3 -s -D")
    # Запуск iperf клиента на первом хосте, соединяющегося со вторым хостом
    h1.cmd(f"mkdir -p output/{host1_name}_to_{host2_name}")
    h1.cmdPrint(f'iperf3 -c {h2.IP()} -t 26 -J > output/{host1_name}_to_{host2_name}/{host1_name}_to_{host2_name}_iperf3.json')
    h1.cmd(f"cd output/{host1_name}_to_{host2_name} && plot_iperf.sh {host1_name}_to_{host2_name}_iperf3.json")


def monitor_queue(net, interface="r0-eth2", interval=1, output_file='queue_monitor.log'):
    t = threading.currentThread()
    with open(output_file, 'w') as file:
        while getattr(t, "do_run", True):
            result = net['r0'].cmd(f'tc -s qdisc show dev {interface}')
            print(result, file=file)
            time.sleep(interval)




def run(num_hosts_subnets=20):
    topo = NetworkTopo(num_hosts_subnets=20)
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r0'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r0-eth2"))
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r1-eth2"))
    #установка типа окна TCP и ее размера
    info(net['c0'].cmd("sudo sysctl -w net.ipv4.tcp_congestion_control=reno"))
    info(net['c0'].cmd("sudo sysctl -w net.ipv4.tcp_rmem='2000 8000 16000'"))
    info(net['c0'].cmd("sudo sysctl -w net.ipv4.tcp_wmem='2000 8000 16000'"))

    
    
    
    #установка задержек на соединениях с помощью netem
    for i in range(1, 2*num_hosts_subnets + 1):
	    host = net.get(f'h{i}')  # Генерируем имя хоста на основе i
	    if (i%2==1):
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 20ms")
	    else:
	     host.cmd(f"sudo tc qdisc add dev h{i}-eth0 root netem delay 15ms") 


    #настройка алгоритма RED
    avpkt = 500
    limit = avpkt * 300
    min_ = avpkt * 75
    max_ = avpkt * 150
    probability = 0.1
    bandwidth = 20
    #burst = 125

    net['r0'].cmdPrint("tc qdisc add dev r0-eth2 root handle 1: red limit {} min {} max {} avpkt {} bandwidth {} probability {}".format(limit, min_, max_, avpkt, bandwidth, probability))

    net.start()
    threads = []
            
    # Пример: запуск iperf между несколькими парами хостов
    for i in range(1, 2*num_hosts_subnets, 2):
        host1 = f'h{i}'
        host2 = f'h{i+1}'
        t = Thread(target=run_iperf, args=(net, host1, host2))
        t.start()
        threads.append(t)
        
        
  
    # Ожидание завершения всех потоков
    for t in threads:
        t.join()
    
       
    #Мониторинг параметров RED    
    print(net['r0'].cmd("tc -s qdisc show dev r0-eth2"))
    #CLI(net)
    net.stop() # Остановка сети


#запуск программы
if __name__ == '__main__':
    setLogLevel('info')
    run()

