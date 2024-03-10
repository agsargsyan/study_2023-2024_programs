#!/usr/bin/gnuplot -persist


set style line 1 lt 1 lw 1 lc rgb "black"   
set style line 2 lt 2 lw 1 lc rgb "black" dashtype (1,3) 

set terminal pdf
set output "plots/queues.pdf"
set xlabel "Время (в секундах)"
set ylabel "Длина очереди (в пакетах)"
set title "Имитационная модель с RED"
plot "output/temp.q" with lines linestyle 1 title "Длина очереди", "output/temp.a" with lines linestyle 2 title "Средняя длина очереди"

set terminal pdf
set output "plots/cwnd.pdf"
set xlabel "Время (в секундах)"
set ylabel "Размер окна TCP (в пакетах)"
set title "TCPVsWindow"
plot "output/WvsT" with lines linestyle 1 lt 1 lw 2 lc rgb "black" title "WvsT"

set terminal pdf
set output "plots/cwnd_1.pdf"
set xlabel "Время (в секундах)"
set ylabel "Размер окна TCP для 1 источника (в пакетах)"
set title "TCPVsWindow_1"
plot "output/WvsT_1" with lines linestyle 1 lt 1 lw 2 lc rgb "black" title "WvsT"

set terminal pdf
set output "plots/RTT.pdf"
set xlabel "Время (в секундах)"
set ylabel "RTT (в секундах)"
set title "RTT"
plot "output/RTT" with lines linestyle 1 lt 1 lw 2 lc rgb "black" title "RTT"

set terminal pdf
set output "plots/RTTVAR.pdf"
set xlabel "Время (в секундах)"
set ylabel "RTTVAR (в секундах)"
set title "RTTVAR"
plot "output/RTTVAR" with lines linestyle 1 lt 1 lw 2 lc rgb "black" title "RTTVAR"
