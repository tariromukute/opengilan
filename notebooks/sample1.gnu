set style data linespoints
set key autotitle columnhead
set datafile separator ','
set title "Sample graph"
set grid xtics ytics mytics
set xlabel "Year"
set ylabel "Sales"
plot for [i=2:3] "sample1.csv" u 1:i t columnhead