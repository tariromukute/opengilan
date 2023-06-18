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

We can check the `/proc` to see if the flags that were sent for the epoll events. We will need to do this in two steps (i) get the file descriptors for epoll `bpftrace -e 't:syscalls:sys_enter_epoll_wait { @pid[comm, pid, args->epfd] = count(); }'` or with bcc tools `python3 argdist.py -c -C 'sys_enter_epoll_wait()........'` and then (ii) check if flags set on the file descriptor `cat /proc/[pid]/fdinfo/[epfd]`

## Nanosleep

Possible reasons for high nanosleep syscalls
Check for nanosleep tracepoints `sudo python3 tplist.py | grep nanosleep`
**Interruption due to error**

`sudo python3 argdist.py -C 't:syscalls:sys_exit_nanosleep():u16:args->ret' -i 5 -d 5`
`sudo python3 argdist.py -C 't:syscalls:sys_exit_clock_nanosleep():u16:args->ret' -i 5 -d 5`

## Read/Write

Possible reasons:
- buffer is small
- interrupt error
- latency can due to blocking calls
- using nanosleep in between can have two effects, if smaller a lot of syscalls with nothing,  if large affects performance latency between reads

**buffer is small**

Check the value of count and compare it with SSIZE_MAX and get a histgram for each fd.

```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_read

# Get stats on the bytes read
bpftrace -e 't:syscalls:sys_enter_read { @pid[comm, args->fd, args->count] = count(); }'

# Use bcc tools for above
argdist.py -c -C 't:syscalls:sys_enter_read():int,u32,size_t:$PID,args->fd,args->count'

# Check read buffer size vs read bytes
bpftrace -e '
t:syscalls:sys_enter_read 
{
    @bytes_count[tid] = args->count;
}
t:syscalls:sys_exit_read
/@bytes_count[tid]/
{
    $b = @bytes_count[tid];
    if(args->ret < 0) {
        @err[-args->ret] = count();
    } else {
        @timeout[comm, $b, args->ret] = count();
    }
    delete(@bytes_count[tid]);
}

END
{
    clear(@bytes_count);
}
'
```

Write operations

```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_write

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_enter_write { @pid[comm, args->fd, args->count] = count(); }'

# Use bcc tools for above
argdist.py -c -C 't:syscalls:sys_enter_write():int,u32,size_t:$PID,args->fd,args->count'

# Check write buffer size vs written bytes
bpftrace -e '
t:syscalls:sys_enter_write 
{
    @bytes_count[tid] = args->count;
}
t:syscalls:sys_exit_write
/@bytes_count[tid]/
{
    $b = @bytes_count[tid];
    if(args->ret < 0) {
        @err[-args->ret] = count();
    } else {
        @timeout[comm, $b, args->ret] = count();
    }
    delete(@bytes_count[tid]);
}

END
{
    clear(@bytes_count);
}
'
```

## recv, recvfrom, recvmsg, recvmmsg
`sudo python3 tplist.py | grep recv`

For recvfrom
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_recvfrom
sudo python3 tplist.py -v syscalls:sys_exit_recvfrom

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_recvfrom { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_recvfrom():int,long:$PID,args->ret'
```

For recvmsg

```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_recvmsg
sudo python3 tplist.py -v syscalls:sys_exit_recvmsg

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_recvmsg { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_recvmsg():int,long:$PID,args->ret'
```

For recvmmsg

```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_recvmmsg
sudo python3 tplist.py -v syscalls:sys_exit_recvmmsg

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_recvmmsg { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_recvmmsg():int,long:$PID,args->ret'
```

**Check if sockets are set to non-blocking**
`sudo python3 tplist.py | grep socket` and `sudo python3 tplist.py | grep accept`

For socket, client side
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_socket
sudo python3 tplist.py -v syscalls:sys_enter_socketpair

# On socket family contains the flags
# Check if set to non-blocking with argdist
argdist.py -c -C 't:syscalls:sys_enter_socket():int,int,int:$PID,args->protocol,args->family&00004000'
```

For accept4, server side
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_accept4

# Check if set to non-blocking with argdist
argdist.py -c -C 't:syscalls:sys_enter_accept4():int,int,int:$PID,args->fd,args->flags&00004000'
```
## send, sendto, sendmsg, sendmmsg

`sudo python3 tplist.py | grep send`

For sendto
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_sendto
sudo python3 tplist.py -v syscalls:sys_exit_sendto

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_sendto { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_sendto():int,long:$PID,args->ret'
```

For sendmsg
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_sendmsg
sudo python3 tplist.py -v syscalls:sys_exit_sendmsg

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_sendmsg { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_sendmsg():int,long:$PID,args->ret'
```

For sendmmsg
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_sendmmsg
sudo python3 tplist.py -v syscalls:sys_exit_sendmmsg

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_sendmmsg { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_sendmmsg():int,long:$PID,args->ret'
```

## open, openat

`sudo python3 tplist.py | grep open`

For open
```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_open
sudo python3 tplist.py -v syscalls:sys_exit_open

# Check if it is set to non-blocking
bpftrace -e 't:syscalls:sys_enter_open { @pid[comm, pid, args->flags] = count(); }'

# Check if set to non-blocking with argdist
argdist.py -c -C 't:syscalls:sys_enter_open():int,char*,int:$PID,args->filename,args->flags&00004000'

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_open { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_open():int,long:$PID,args->ret'
```

For openat

```bash
# Check args for read syscall
sudo python3 tplist.py -v syscalls:sys_enter_open
sudo python3 tplist.py -v syscalls:sys_exit_open

# Check if it is set to non-blocking
bpftrace -e 't:syscalls:sys_enter_open { @pid[comm, pid, args->flags] = count(); }'

# Check if set to non-blocking with argdist O_NONBLOCK = 00004000
argdist.py -c -C 't:syscalls:sys_enter_openat():int,char*,int:$PID,args->filename,args->flags&00004000'

# Get stats on the bytes written
bpftrace -e 't:syscalls:sys_exit_open { @pid[comm, pid, args->ret] = count(); }'

# Get using argdist, but it doesn't give the process name
argdist.py -c -C 't:syscalls:sys_exit_open():int,long:$PID,args->ret'
```
