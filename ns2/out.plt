#!/usr/bin/gnuplot -persist


set terminal postscript eps
set output "plots/queues.eps"
set xlabel "Time, s"
set ylabel "Queue Length [pkt]"
set title "RED Queue"
plot "output/temp.q" with lines linestyle 1 lt 1 lw 2 title "Queue length", "output/temp.a" with lines linestyle 2 lt 3 lw 2 title "Average queue length"

set terminal postscript eps
set output "plots/cwnd.eps"
set xlabel "Time (s)"
set ylabel "Window size [pkt]"
set title "TCPVsWindow"
plot "output/WvsT" with lines linestyle 1 lt 1 lw 2 title "WvsT"

set terminal postscript eps
set output "plots/cwnd_1.eps"
set xlabel "Time (s)"
set ylabel "Window size in 1st source [pkt]"
set title "TCPVsWindow_1"
plot "output/WvsT_1" with lines linestyle 1 lt 1 lw 2 title "WvsT"

set terminal postscript eps
set output "plots/RTT.eps"
set xlabel "Time (s)"
set ylabel "RTT (s)"
set title "RTT"
plot "output/RTT" with lines linestyle 1 lt 1 lw 2 title "RTT"

set terminal postscript eps
set output "plots/RTTVAR.eps"
set xlabel "Time (s)"
set ylabel "RTTVAR (s)"
set title "RTTVAR"
plot "output/RTTVAR" with lines linestyle 1 lt 1 lw 2 title "RTTVAR"
