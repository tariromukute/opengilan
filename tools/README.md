# Development of tools for investigating performance of syscall

## epoll

Possible reasons high freq of epoll syscalls

**ready file descriptors more than maxevents**
We can confirm this by comparing the reads events vs the maximum events. There are two tracepoints for epoll_wait, `syscalls:sys_enter_epoll_wait` and `syscalls:sys_exit_epoll_wait` that contain the information. We can inspect each using the argdist tool, but correlating the output is not natively available. To get more details on the syscalls:
- Discover format for the entrypoint: `sudo python3 tplist.py -v syscalls:sys_enter_epoll_wait`
- Discover format for the exit: `sudo python3 tplist.py -v syscalls:sys_exit_epoll_wait`

```bash
bpftrace -e '
t:syscalls:sys_enter_epoll_wait 
{
    @epoll_maxevent[tid] = args->maxevents;
}
t:syscalls:sys_exit_epoll_wait
/@epoll_maxevent[tid]/
{
    $m = @epoll_maxevent[tid];
    if(args->ret < 0) {
        @err[-args->ret] = count();
    } else {
        $d = $m - args->ret;
        @diff[$m, $d] = count();
    }
    delete(@epoll_maxevent[tid]);
}

END
{
    clear(@epoll_maxevent);
}
'
```

**timeout value is small or maybe too large**

This means that the intervals for timeout are too small such that in most cases there won't be data available. We can check the values against the number of events returned.

```bash
bpftrace -e '
t:syscalls:sys_enter_epoll_wait 
{
    @epoll_timeout[tid] = args->timeout;
}
t:syscalls:sys_exit_epoll_wait
/@epoll_timeout[tid]/
{
    $t = @epoll_timeout[tid];
    if(args->ret < 0) {
        @err[-args->ret] = count();
    } else {
        @timeout[$t, args->ret] = count();
    }
    delete(@epoll_timeout[tid]);
}

END
{
    clear(@epoll_timeout);
}
'
```

**Need to run in ET**

`sudo python3 argdist.py -C 't:syscalls:sys_enter_epoll_wait():u16:args->epfd' -i 5 -d 5`