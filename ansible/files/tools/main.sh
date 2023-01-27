#!/bin/bash

TOOL_NAME="${1}"
INTERVAL="${2}"
COUNT="${3}"
DURATION="${4}"


function run_tool {
    echo "Run tool called"
    # System
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "syscount" ]; then
        tool="syscount"
        echo "Running syscount -> time spent by tasks on the CPU before being descheduled"
        mkdir -p results/tool=${tool}
        python3 syscount.py -L -j -i ${INTERVAL} -d ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "sysprocess" ]; then
        tool="sysprocess"
        echo "Running sysprocess -> time spent by tasks on the CPU before being descheduled"
        mkdir -p results/tool=${tool}
        python3 syscount.py -L -P -j -i ${INTERVAL} -d ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi

    # CPU
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "oncpudist" ]; then
        tool="oncpudist"
        echo "Running oncpudist -> time spent by tasks on the CPU before being descheduled"
        mkdir -p results/tool=${tool}
        python3 cpudist.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "offcpudist" ]; then
        tool="offcpudist"
        echo "Running offcpudist -> time spent by tasks waiting for their turn to run on-CPU"
        mkdir -p results/tool=${tool}
        python3 cpudist.py -O -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi  
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "profile" ]; then
        tool="profile"
        echo "Running profile -> code paths that are consuming CPU resources"
        mkdir -p "results/tool=${tool}"
        python3 profile.py -adf ${DURATION} > "results/tool=${tool}/${tool}.txt"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "offcputime" ]; then
        tool="offcputime"
        echo "Running offcputime ->  code path resulting in the process being off-CPU"
        mkdir -p results/tool=${tool}
        python3 offcputime.py -fKu ${DURATION} > "results/tool=${tool}/${tool}.txt"
    fi 

    # Memory
    # if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "mmapsnoop" ]; then
    #     tool="mmapsnoop"
    #     echo "Running mmapsnoop -> requests for mappings"
    #     mkdir -p results/tool=${tool}
    #     # not on repo
    #     # python3 mmapsnoop.py ${INTERVAL} ${DURATION} > "results/tool=${tool}/${tool}.json"
    # fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "sys_enter_brk" ]; then
        tool="sys_enter_brk"
        echo "Running t:syscalls:sys_enter_brk ->  code path responsible for heap extension"
        mkdir -p results/tool=${tool}
        # trace -U t:syscalls:sys_enter_brk
        # stackcount -PU t:syscalls:sys_enter_brk
        bpftrace -q -f json -e "tracepoint:syscalls:sys_enter_brk { @[comm] = count(); } interval:s:${DURATION} { exit(); }" > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "page_fault_user" ]; then
        tool="page_fault_user"
        echo "Running t:exceptions:page_fault_user ->  code path responsible for page faults"
        mkdir -p results/tool=${tool}
        python3 stackcount.py -f -PU -D ${DURATION} t:exceptions:page_fault_user > "results/tool=${tool}/${tool}.txt"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "page_fault_kernel" ]; then
        tool="page_fault_kernel"
        echo "Running t:exceptions:page_fault_kernel ->  code path responsible for page faults"
        mkdir -p results/tool=${tool}
        python3 stackcount.py -P -df -D ${DURATION} t:exceptions:page_fault_kernel > "results/tool=${tool}/${tool}.txt"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "drsnoop" ]; then
        tool="drsnoop"
        echo "Running drsnoop -> process affected and the latency: the time taken for the reclaim"
        mkdir -p results/tool=${tool}
        # duration not working
        python3 drsnoop.py -j -d ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi

    # Filesystem
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "ext4dist" ]; then
        tool="ext4dist"
        echo "Running ext4dist -> traces ext4 reads, writes, opens, and fsyncs, and summarizes their latency.
                also includes data presented by vfsstat tool."
        mkdir -p results/tool=${tool}
        python3 ext4dist.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "filetop" ]; then
        tool="filetop"
        echo "Running filetop -> filenames with the most frequent read and writes (includes sockets -a)
                inlcude information from vfssize.bt"
        mkdir -p results/tool=${tool}
        python3 filetop.py -C -a -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "cachestat" ]; then
        tool="cachestat"
        echo "Running cachestat -> the page cache hit ratio over time"
        mkdir -p results/tool=${tool}
        python3 cachestat.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "cachetop" ]; then
        tool="cachetop"
        echo "Running cachetop -> the page cache hit ratio over time"
        echo "Shows Linux page cache hit/miss statistics including read and write hit % per process."
        mkdir -p results/tool=${tool}
        python3 cachetop.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi

    # Disk I/O
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "biolatency" ]; then
        tool="biolatency"
        echo "Running biolatency -> block I/O device latency"
        echo "The latency of the disk I/O is measured from the issue to the device to its
                completion. A -Q option can be used to include time queued in the kernel.
                
                The -D option will print a histogram per disk
                
                The -F option prints a separate histogram for each unique set of request"
        
        mkdir -p results/tool=${tool}
        python3 biolatency.py -Q -F -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "biotop" ]; then
        tool="biotop"
        echo "Running biotop -> block device I/O top"
        echo "Summary of processes which are performing disk I/O. This only shows the top 20 processes (-r 20).
                I/O gives the number read/write (rwflag) operations peformed by process X (name) in the interval.
                The tool also gives the total kbytes of the I/O operations.

                The -C option can be used to prevent the screen from clearing"
        
        mkdir -p results/tool=${tool}
        python3 biotop.py -C -j -r 20 ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "bitesize" ]; then
        tool="bitesize"
        echo "Running bitesize -> processes performing I/O on disk and the bite-size"
        mkdir -p results/tool=${tool}
        python3 bitesize.py -j -d ${DURATION}  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "iosched" ]; then
        tool="iosched"
        echo "Running iosched -> time requests were queued in the I/O scheduler in the block layer"
        mkdir -p results/tool=${tool}
        # bt and needs kprobe which has been removed
        # bpftrace iosched.bt  > "results/tool=${tool}/${tool}.json"
    fi
    
    # Networking
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "netsize" ]; then
        tool="netsize"
        echo "Running netsize -> number of packets being received and their size"
        mkdir -p results/tool=${tool}
        # needs etj name and converted to json
        bpftrace -q -f json netsize.bt > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "nettxlat-dev" ]; then
        echo "Running nettxlat-dev -> latency of the device queue"
        tool="nettxlat-dev"
        mkdir -p results/tool=${tool}
        # bt
        # Having issues with duplicate device names
        # bpftrace -q -f json nettxlat-dev.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "qdisc-fq" ]; then
        echo "Running qdisc-fq -> time spent on the queuing disciplines"
        tool="qdisc-fq"
        mkdir -p results/tool=${tool}
        # bt needs kprobe which was removed
        # bpftrace qdisc-fq.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "skblife" ]; then
        tool="skblife"
        echo "Running skblife -> lifespan of the kernel buffers"
        mkdir -p results/tool=${tool}
        bpftrace -q -f json skblife.bt  > "results/tool=${tool}/${tool}.json"
    fi

    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "softirqs_count" ]; then
        tool="softirqs_count"
        echo "Running softirqs_count"
        mkdir -p "results/tool=${tool}"
        python3 softirqs.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "softirqs_dist" ]; then
        tool="softirqs_dist"
        echo "Running softirqs_dist"
        mkdir -p "results/tool=${tool}"
        python3 softirqs.py -d -j  ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "hardirqs_count" ]; then
        tool="hardirqs_count"
        echo "Running hardirqs_count"
        mkdir -p "results/tool=${tool}"
        python3 hardirqs.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "hardirqs_dist" ]; then
        tool="hardirqs_dist"
        echo "Running hardirqs_dist"
        mkdir -p "results/tool=${tool}"
        python3 hardirqs.py -d -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi

    # TCP 
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "tcplife" ]; then
        tool="tcplife"
        echo "Running tcplife -> lifespan of the tcp connections"
        mkdir -p results/tool=${tool}
        python3 tcplife.py -j -d ${DURATION}  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "tcpconnlat" ]; then
        tool="tcpconnlat"
        echo "Running tcpconnlat -> latency of tcp connections"
        mkdir -p results/tool=${tool}
        python3 tcpconnlat.py -j -d ${DURATION}  > "results/tool=${tool}/${tool}.json"
    fi

    # Collect network traffic
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "tcpdump" ]; then
        tool="tcpdump"
        echo "Running tcpdump"
        mkdir -p "results/tool=${tool}"
        timeout  ${INTERVAL} tcpdump -eni ens3 -A -w "results/tool=${tool}/${tool}.pcap"
    fi

}

function main {
    run_tool
}

main