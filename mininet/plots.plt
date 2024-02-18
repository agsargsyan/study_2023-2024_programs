set terminal pdf
set output 'results/RTT.pdf'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "RTT (sec)"
set yrange [0:*]
set title "RTT over time"
unset key
set grid
set style data lines
FILES = system("ls -1 *.dat")
plot for [data in FILES] data u 2:($8/1000) with lines linecolor rgb "black" notitle



set terminal pdf
set output 'results/cwnd.pdf'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "Cwnd"
set yrange [0:*]
set title "Sent Cwnd over time"
unset key
set grid
set style data lines
FILES = system("ls -1 *.dat")
plot for [data in FILES] data u 2:7 with lines linecolor rgb "black" notitle



set terminal pdf
set output 'results/RTT_Var.pdf'
set datafile separator " "
set xlabel "Time (sec)"
set ylabel "RTT Var (sec)"
set yrange [0:*]
set title "RTT Var over time"
unset key
set grid
set style data lines
FILES = system("ls -1 *.dat")
plot for [data in FILES] data u 2:($9/1000) with lines linecolor rgb "black" notitle

