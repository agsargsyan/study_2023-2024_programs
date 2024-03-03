#!/usr/bin/gnuplot -persist

set xrange [0:25]



#set terminal postscript eps
set terminal pdf
set encoding utf8
set output "tcp.pdf"

set xlabel "Время (в секундах)"
set ylabel "Размер окна TCP (в пакетах)"
set title "Размер окна перегрузки при разных TCP"

# Определение стилей линий
set style line 1 lt 1 lw 1 lc rgb "black" dashtype (5,2,2,2)  # Newreno
set style line 2 lt 2 lw 1 lc rgb "black" dashtype (1,3) # Reno с использованием dashtype
set style line 3 lt 5 lw 1 lc rgb "black"  # Vegas

# Построение графика с использованием определенных стилей линий
plot "WvsT_1_Newreno" with lines linestyle 1 title "Newreno", \
     "WvsT_1_Reno" with lines linestyle 2 title "Reno", \
     "WvsT_1_Vegas" with lines linestyle 3 title "Vegas"


#!/usr/bin/gnuplot -persist
#set terminal postscript eps
set terminal pdf
set encoding utf8
set output "red1.pdf"

set xlabel "Время (в секундах)"
set ylabel "Длина очереди (в пакетах)"
set title "Размер очереди на линке при разных RED"

# Определение стилей линий
set style line 3 lt 1 lw 1 lc rgb "black" dashtype (5,2,2,2)  
set style line 2 lt 2 lw 1 lc rgb "black" dashtype (1,3) 
set style line 1 lt 5 lw 1 lc rgb "black"
set style line 4 lt 1 lw 1 lc rgb "black" dashtype (2,5,1,5) # Штрих-пунктирная линия   

# Построение графика с использованием определенных стилей линий
plot "classic.a" with lines linestyle 1 title "Classic", \
     "dsred.a" with lines linestyle 2 title "Double-slope", \
     "gentle.a" with lines linestyle 3 title "Gentle", \
     "nlred.a" with lines linestyle 4 title "NLRED"


#!/usr/bin/gnuplot -persist
#set terminal postscript eps
set terminal pdf
set encoding utf8
set output "red2.pdf"

set xlabel "Время (в секундах)"
set ylabel "Длина очереди (в пакетах)"
set title "Размер очереди на линке при адаптивных RED"

# Определение стилей линий

set style line 3 lt 1 lw 1 lc rgb "black" dashtype (5,2,2,2)  
set style line 2 lt 2 lw 1 lc rgb "black" dashtype (1,3) 
set style line 1 lt 5 lw 1 lc rgb "black
set style line 4 lt 1 lw 2 lc rgb "black" dashtype (2,5,1,5) # Штрих-пунктирная линия 

# Построение графика с использованием определенных стилей линий
plot "ared.a" with lines linestyle 1 title "Floyd's adaptive", \
     "feng.a" with lines linestyle 2 title "Feng's adaptive", \
     "refined.a" with lines linestyle 3 title "Refined adaptive", \
     "powared.a" with lines linestyle 4 title "Powared"
