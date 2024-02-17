#новый экземпляр объекта Symulator
set ns [new Simulator]

#трейс файл для nam, файл слишком большой, так что временно закомментируем
set nf [open output/out.nam w]
$ns namtrace-all $nf

#количество источников 
set N 20

#создание узлов
source "nodes.tcl"

#метрики TCP
source "TCP.tcl"

#настройка очереди		
source "queue.tcl"

#настройка времени моделирования  		
source "timing.tcl" 		

#визуализация в nam
source "nam.tcl"   		

#процедура finish
source "finish.tcl"                                                                         

#запуск программы
$ns run

 
