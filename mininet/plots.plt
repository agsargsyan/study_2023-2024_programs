set terminal postscript eps
set output 'results/RTT.eps'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "RTT (sec)"
set yrange [0:*]
set title "RTT over time"
unset key
set grid
set style data lines
FILES = system("ls -1 combined.dat")
plot for [data in FILES] data u 2:($8/1000) with lines linecolor rgb "black" notitle



set terminal postscript eps
set output 'results/cwnd.eps'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "Cwnd [pkt]"
set yrange [0:*]
set title "Sent Cwnd over time"
unset key
set grid
set style data lines
FILES = system("ls -1 combined.dat")
plot for [data in FILES] data u 2:($7/1000) with lines linecolor rgb "black" notitle

set terminal postscript eps
set output 'results/cwnd1.eps'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "Cwnd [pkt]"
set yrange [0:*]
set title "Sent Cwnd over time"
unset key
set grid
set style data lines
FILES = system("ls -1 output/h1_to_h2/results/1.dat")
plot for [data in FILES] data u 2:($7/1000) with lines linecolor rgb "black" notitle



set terminal postscript eps
set output 'results/RTT_Var.eps'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "RTT Var (sec)"
set yrange [0:*]
set title "RTT Var over time"
unset key
set grid
set style data lines
FILES = system("ls -1 combined.dat")
plot for [data in FILES] data u 2:($9/1000) with lines linecolor rgb "black" notitle


set terminal postscript eps
set output 'results/queue.eps'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "Queue length [pkt]"
set title "Queue length over time"
set style data lines
set yrange [0:*]
FILES = system("ls -1 queue.dat")
plot for [data in FILES] data u 1:8 with lines linecolor rgb "black" notitle
