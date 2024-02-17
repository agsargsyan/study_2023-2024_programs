# Мониторинг метрик TCP

#размер окна TCP для всех источников
set windowVsTime [open output/WvsT w]

#размер окна TCP для 1 источника 
set windowVsTime_1 [open output/WvsT_1 w]

#время приема-передачи
set rtt [open output/RTT w]

#отклонение времени приема-передачи 
set rttvar [open output/RTTVAR w]


# Функция для получение данных о метриках
proc plotMetric {tcpSource file metric} {
    global ns
    set time 0.01
    set now [$ns now]
    set value [$tcpSource set $metric]
    puts $file "$now $value"
    $ns at [expr $now+$time] "plotMetric $tcpSource $file $metric"
}
