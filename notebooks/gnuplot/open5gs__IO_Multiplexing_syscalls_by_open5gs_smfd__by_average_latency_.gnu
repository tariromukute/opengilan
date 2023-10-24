set style data linespoints
set term png
set output 'open5gs__IO_Multiplexing_syscalls_by_open5gs_smfd__by_average_latency_.png'
set key noenhanced
set key top left
set key autotitle columnhead
set datafile separator ','
set title "open5gs: IO Multiplexing syscalls by open5gs-smfd (by average latency)"
set grid xtics ytics mytics
set xlabel "Number of UEs"
set ylabel "Average time per syscall (ms)"
 # Create theme 
         dpi = 600 ## dpi (variable) 
         width = 164.5 ## mm (variable) 
         height = 100 ## mm (variable) 
         
         in2mm = 25.4 # mm (fixed) 
         pt2mm = 0.3528 # mm (fixed) 
         
         mm2px = dpi/in2mm 
         ptscale = pt2mm*mm2px 
         round(x) = x - floor(x) < 0.5 ? floor(x) : ceil(x) 
         wpx = round(width * mm2px) 
         hpx = round(height * mm2px) 
         
         set terminal pngcairo size wpx,hpx fontscale ptscale/1.4 linewidth ptscale pointscale ptscale 
         
         colors = "blue red green brown black magenta orange purple sienna1 slategray tan1 yellow turquoise orchid khaki" 
 plot for [i=2:3] "open5gs__IO_Multiplexing_syscalls_by_open5gs_smfd__by_average_latency_.csv" u 1:i t columnhead lc rgb word(colors, i-1)