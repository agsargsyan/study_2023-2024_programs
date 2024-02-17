#Создать новый экземпляр объекта Symulator
set ns [new Simulator]

#Открыть трейс файл для nam, файл слишком большой, так что временно закомментируем
set nf [open output/out.nam w]
$ns namtrace-all $nf

#количество источников 
set N 20

#создание узлов
#маршрутизаторы
set node_(r0) [$ns node]  
set node_(r1) [$ns node]  

#источники и приемники
for {set i 0} {$i < $N} {incr i} {
	set node_(s$i) [$ns node] 		
	set node_(s[expr $N + $i]) [$ns node]	
	}

#линки между маршрутизаторами и другими узлами(размер буфера, время, тип очереди)
for {set i 0} {$i < $N} {incr i} {
	$ns duplex-link $node_(s$i) $node_(r0) 100Mb 20ms DropTail
	$ns duplex-link $node_(s[expr $N + $i]) $node_(r1) 100Mb 20ms DropTail
}

#линки между маршрутизаторами(размер буфера, время, тип очереди)
$ns simplex-link $node_(r0) $node_(r1) 20Mb 15ms RED
$ns simplex-link $node_(r1) $node_(r0) 15Mb 20ms DropTail

# Агенты и приложения
for {set t 0} {$t < $N} {incr t} {
	$ns color $t green
	set tcp($t) [$ns create-connection TCP/Reno $node_(s$t) TCPSink $node_(s[expr $N + $t]) $t]
	$tcp($t) set window_ 32
	$tcp($t) set maxcwnd_ 32
	set ftp($t) [$tcp($t) attach-source FTP]
}
 

#метрики TCP
# Мониторинг метрик TCP
set windowVsTime [open output/WvsT w]
set windowVsTime_1 [open output/WvsT_1 w]
set rtt [open output/RTT w]
set rttvar [open output/RTTVAR w]
set qmon [$ns monitor-queue $node_(r0) $node_(r1) [open output/qm.out w]]
[$ns link $node_(r0) $node_(r1)] queue-sample-timeout


# Функция для отрисовки метрик
proc plotMetric {tcpSource file metric} {
    global ns
    set time 0.01
    set now [$ns now]
    set value [$tcpSource set $metric]
    puts $file "$now $value"
    $ns at [expr $now+$time] "plotMetric $tcpSource $file $metric"
}

#очередь		
#Лимит очереди
$ns queue-limit $node_(r0) $node_(r1) 300
$ns queue-limit $node_(r1) $node_(r0) 300

# Мониторинг очереди:
set redq [[$ns link $node_(r0) $node_(r1)] queue]
$redq set thresh_ 75
$redq set maxthresh_ 150
$redq set q_weight_ 0.002
$redq set linterm_ 10
$redq set drop-tail_ true

$redq set queue-in-bytes false
set tchan_ [open output/all.q w]
$redq trace curq_
$redq trace ave_
$redq attach $tchan_


$redq set gentle_ false 

#настройка времени моделирования  		
for {set r 0} {$r < $N} {incr r} {
	$ns at 0.0 "$ftp($r) start"
	$ns at 24.0 "$ftp($r) stop"
	$ns at 1.0 "plotMetric $tcp($r) $windowVsTime cwnd_"
}
$ns at 1.0 "plotMetric $tcp(1) $windowVsTime_1 cwnd_"
$ns at 1.0 "plotMetric $tcp(1) $rtt rtt_"
$ns at 1.0 "plotMetric $tcp(1) $rttvar rttvar_"
$ns at 25.0 "finish"
		

#визуализация
#визуализация цветов, формы, располажения узлов в nam
$node_(r0) color "red"
$node_(r1) color "red"
$node_(r0) label "RED"
$node_(r1) shape "square"
$node_(r0) label "square"

$ns simplex-link-op $node_(r0) $node_(r1) orient right
$ns simplex-link-op $node_(r1) $node_(r0) orient left
$ns simplex-link-op $node_(r0) $node_(r1) queuePos 0
$ns simplex-link-op $node_(r1) $node_(r0) queuePos 0

for {set m 0} {$m < $N} {incr m} {
	$ns duplex-link-op $node_(s$m) $node_(r0) orient right
	$ns duplex-link-op $node_(s[expr $N + $m]) $node_(r1) orient left 
}

for {set i 0} {$i < $N} {incr i} {
	$node_(s$i) color "blue"
	$node_(s$i) label "ftp"

}  		

#процедура finish
#Finish procedure
proc finish {} {
   global ns nf
   $ns flush-trace
   close $nf
   global tchan_
   set awkCode {
      {
	 if ($1 == "Q" && NF>2) {
	    print $2, $3 >> "output/temp.q";
	    set end $2
	 }
	 else if ($1 == "a" && NF>2)
	 print $2, $3 >> "output/temp.a";
      }
   }

   set f [open output/temp.queue w]
   puts $f "TitleText: RED"
   puts $f "Device: Postscript"

   if { [info exists tchan_] } {
      close $tchan_
   }

   exec rm -f output/temp.q output/temp.a output/maxp
   exec touch output/temp.a output/temp.q

   exec awk $awkCode output/all.q

   puts $f \"queue
   exec cat output/temp.q >@ $f
   puts $f \n\"ave_queue
   exec cat output/temp.a >@ $f
   close $f

   exec xgraph -bb -tk -x time -t "TCPRenoCWND" output/WvsT &
   exec xgraph -bb -tk -x time -t "TCPRenoCWND_1" output/WvsT_1 &
   exec xgraph -bb -tk -x time -t "RTT" output/RTT &
   exec xgraph -bb -tk -x time -t "RTTVAR" output/RTTVAR &
   exec xgraph -bb -tk -x time -y queue output/temp.queue &
   #exec nam output/out.nam &
   exit 0
}



                                                                          

#Запуск программы
$ns run

 
