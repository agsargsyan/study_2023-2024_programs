#Лимит очереди
$ns queue-limit $node_(r0) $node_(r1) 300
$ns queue-limit $node_(r1) $node_(r0) 300

#настройка параметров RED
set redq [[$ns link $node_(r0) $node_(r1)] queue]
$redq set thresh_ 75 
$redq set maxthresh_ 150
$redq set q_weight_ 0.002
$redq set linterm_ 10
$redq set drop-tail_ true
#$redq set gentle_ false
$redq set queue-in-bytes false

#мониторинг параметров длины очереди:
set tchan_ [open output/all.q w]
$redq trace curq_
$redq trace ave_
$redq attach $tchan_

#монитринг соеденения между маршрутизаторами
set qmon [$ns monitor-queue $node_(r0) $node_(r1) [open output/qm.out w]] 
[$ns link $node_(r0) $node_(r1)] queue-sample-timeout

#Для реализации разных модификаций RED, реализовано благодаря изменению исходного кода программы

#$redq set nonlinear_ 1
#$redq set hyperbola_ 1 
#$redq set quadratic_linear_ 1
#$redq set three_sections_ 1
#$redq set exponential_ 1
#$redq set smart_ 1
#$redq set double_slope_ 1

#Группа адаптивных алгоритмов
$redq set adaptive_ 1
#$redq set feng_adaptive_ 1
#$redq set refined_adaptive_ 1
#$redq set fast_adaptive_ 1
$redq set powared_ 1

