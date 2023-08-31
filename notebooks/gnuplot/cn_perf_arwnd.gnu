set style data linespoints
set term png
set output 'cn_perf_arwnd.png'
set key top left
set key autotitle columnhead
set datafile separator ','
set title "Average UE completion time"
set grid xtics ytics mytics
set xlabel "Number of UEs"
set ylabel "Window size (bytes)"

set colorsequence classic
set terminal pngcairo enhanced font "arial,10" fontscale 1.0 size 500, 300

colors = "blue red green yellow"


plot for [i=2:4] "cn_perf_arwnd.csv" u 1:i t columnhead lc rgb word(colors, i-1)