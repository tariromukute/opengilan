#!/bin/bash

TOOL_NAME="${1}"
INTERVAL="${2}"
COUNT="${3}"
DURATION="${4}"


function run_tool {
    echo "Run tool called"
    # CPU
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "exitsnoop" ]; then
        tool="exitsnoop"
        echo "Running exitsnoop -> the processes that have run and their age/lifespan"
        mkdir -p results/tool=${tool}
        # needs duration
        # python3 exitsnoop.py > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "runqlat" ]; then
        tool="runqlat"
        echo "Running runqlat -> time each of the processes spends waiting for its turn on CPU"
        mkdir -p results/tool=${tool}
        python3 runqlat.py ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
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
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "llcstat" ]; then
        tool="llcstat"
        echo "Running llcstat -> number of cache misses of the LLC and the hit ratios of the LLC (this can't run on a virtual machine)"
        mkdir -p results/tool=${tool}
        python3 llcstat.py ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi 

    # Memory
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "mmapsnoop" ]; then
        tool="mmapsnoop"
        echo "Running mmapsnoop -> requests for mappings"
        mkdir -p results/tool=${tool}
        # not on repo
        # python3 mmapsnoop.py ${INTERVAL} ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "sys_enter_brk" ]; then
        tool="sys_enter_brk"
        echo "Running t:syscalls:sys_enter_brk ->  code path responsible for heap extension"
        mkdir -p results/tool=${tool}-kernel
        # trace -U t:syscalls:sys_enter_brk
        # stackcount -PU t:syscalls:sys_enter_brk
        bpftrace -q -f json -e "tracepoint:syscalls:sys_enter_brk { @[comm] = count(); } interval:s:${DURATION} { exit(); }" > "results/tool=${tool}-kernel/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "page_fault" ]; then
        tool="page_fault"
        echo "Running t:exceptions:page_fault* ->  code path responsible for page faults"
        mkdir -p results/tool=${tool}-user
        mkdir -p results/tool=${tool}-kernel
        python3 stackcount.py -f -PU -D ${DURATION} t:exceptions:page_fault_user > "results/tool=${tool}-user/${tool}.txt"
        python3 stackcount.py -P -df -D ${DURATION} t:exceptions:page_fault_kernel > "results/tool=${tool}-kernel/${tool}.txt"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "drsnoop" ]; then
        tool="drsnoop"
        echo "Running drsnoop -> process affected and the latency: the time taken for the reclaim"
        mkdir -p results/tool=${tool}
        # duration not working
        # python3 drsnoop.py -d ${DURATION} > "results/tool=${tool}/${tool}.json"
    fi

    # Filesystem
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "vfsstat" ]; then
        tool="vfsstat"
        echo "Running vfsstat -> characterization virtual file system operations"
        mkdir -p results/tool=${tool}
        python3 vfsstat.py ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi 
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "vfssize" ]; then
        tool="vfssize"
        echo "Running vfssize -> read and write operations by the process names"
        mkdir -p results/tool=${tool}

        bpftrace -q -f json vfssize.bt ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi 
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "filetop" ]; then
        tool="filetop"
        echo "Running filetop -> filenames with the most frequent read and writes (includes sockets -a)"
        mkdir -p results/tool=${tool}
        python3 filetop.py -C -a ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "cachestat" ]; then
        tool="cachestat"
        echo "Running cachestat -> the page cache hit ratio over time"
        mkdir -p results/tool=${tool}
        python3 cachestat.py ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi

    # Disk I/O
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "biolatency" ]; then
        tool="biolatency"
        echo "Running biolatency -> block I/O device latency"
        mkdir -p results/tool=${tool}
        python3 biolatency.py -j ${INTERVAL} ${COUNT} > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "bitesize" ]; then
        tool="bitesize"
        echo "Running bitesize -> processes performing I/O on disk and the bite-size"
        mkdir -p results/tool=${tool}
        # needs duration and json output
        # python3 bitesize.py  > "results/tool=${tool}/${tool}.json"
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
        bpftrace -q -f json nettxlat-dev.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "qdisc-fq" ]; then
        echo "Running qdisc-fq -> time spent on the queuing disciplines"
        tool="qdisc-fq"
        mkdir -p results/tool=${tool}
        # bt needs kprobe which was removed
        # bpftrace qdisc-fq.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "soconnect" ]; then
        tool="soconnect"
        echo "Running soconnect -> latency for IP protocol connections and the process making the connection"
        mkdir -p results/tool=${tool}
        # Format needs to be sorted to json
        bpftrace -q soconnect.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "skblife" ]; then
        tool="skblife"
        echo "Running skblife -> lifespan of the kernel buffers"
        mkdir -p results/tool=${tool}
        bpftrace -q -f json skblife.bt  > "results/tool=${tool}/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "sormem" ]; then
        tool="sormem"
        echo "Running sormem -> the number of packets and allocated size of the socket buffers and their limits"
        mkdir -p results/tool=${tool}
        bpftrace -q -f json sormem.bt  > "results/tool=${tool}/${tool}.json"
    fi

    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "softirqs" ]; then
        tool="softirqs"
        echo "Running softirqs"
        mkdir -p "results/tool=${tool}-count"
        mkdir -p "results/tool=${tool}-dist"
        python3 softirqs.py ${INTERVAL} ${COUNT} > "results/tool=${tool}-count/${tool}.json"
        python3 softirqs.py -d  ${INTERVAL} ${COUNT} > "results/tool=${tool}-dist/${tool}.json"
    fi
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "hardirqs" ]; then
        tool="hardirqs"
        echo "Running hardirqs"
        mkdir -p "results/tool=${tool}-count"
        mkdir -p "results/tool=${tool}-dist"
        python3 hardirqs.py ${INTERVAL} ${COUNT} > "results/tool=${tool}-count/${tool}.json"
        python3 hardirqs.py -d  ${INTERVAL} ${COUNT} > "results/tool=${tool}-dist/${tool}.json"
    fi

    # Collect network traffic
    if  [ "${TOOL_NAME}" = "all" ] || [ "${TOOL_NAME}" = "tcpdump" ]; then
        tool="tcpdump"
        echo "Running tcpdump"
        mkdir -p "results/tool=${tool}"
        timeout  ${INTERVAL} tcpdump -eni eth1 -A -w "results/tool=${tool}/${tool}.pcap"
    fi

}

function main {
    run_tool
}

main