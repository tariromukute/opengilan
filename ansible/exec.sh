
# This script is used to execute the commands in to run ansible ad hoc commands
# and playbooks.

# List of syscalls to inspect
NX="0 100 200 300 400 500 600 900"
for N_UES in $NX; do
# SYSCALLS="futex epoll_wait recvmsg clock_nanosleep poll select ppoll read openat sendto sched_yield recvfrom fdatasync write nanosleep io_getevents epoll_pwait rt_sigtimedwait"
SYSCALLS="io_getevents epoll_pwait rt_sigtimedwait"
# Loop through the syscalls and run the ansible ad hoc commands with syscall as parameter
# ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/oai-1.yml \
#     -e '{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: "syscount.py -d 20 -L -m -j", tool: syscount, ues: '$N_UES' }'

# ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/oai-1.yml \
#     -e '{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: "syscount.py -d 20 -L -P -m -j", tool: sysprocess, ues: '$N_UES' }'

# for SYSCALL in $SYSCALLS; do
#     ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/oai-1.yml \
#     -e '{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: "syscount.py --syscall '$SYSCALL' -d 20 -L -P -m -j", tool: sysprocess_'$SYSCALL', ues: '$N_UES' }'
# done

# ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/oai-1.yml \
#     -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -C 't:syscalls:sys_enter_epoll_wait():u16:args->timeout' -i 20 -d 20\", tool: sysprocess_enter_epoll_wait_timeout, ues: "$N_UES" }"

ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -C 't:syscalls:sys_exit_epoll_wait():u16:args->ret' -i 20 -d 20\", tool: sysprocess_exit_epoll_wait, ues: "$N_UES" }"

ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -C 't:syscalls:sys_exit_nanosleep():u16:args->ret' -i 20 -d 20\", tool: sys_exit_nanosleep, ues: "$N_UES" }"

ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -C 't:syscalls:sys_exit_clock_nanosleep():u16:args->ret' -i 20 -d 20\", tool: sys_exit_clock_nanosleep, ues: "$N_UES" }"

# ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/free5gc.yml \
#     -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"trace.py -U -a -A -M 1000 'r::__x64_sys_futex "%d", retval' -i 20 -d 20\", tool: __x64_sys_futex, ues: "$N_UES" }"

ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"klockstat.py -d 20\", tool: sys_exit_clock_nanosleep, ues: "$N_UES" }"

ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -c -C 't:syscalls:sys_enter_socket():int,int,int:$PID,args->protocol,args->family&00004000' -i 20 -d 20\", tool: sys_enter_socket, ues: "$N_UES" }"

PID='$PID'
ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/open5gs.yml \
    -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -c -C 't:syscalls:sys_enter_accept4():int,int,int:$PID,args->fd,args->flags&00004000' -i 20 -d 20\", tool: sys_enter_accept4, ues: "$N_UES" }"
# ansible all -i inventory.ini -u ubuntu -m include_tasks -a file=plays/oai-1.yml \
#     -e "{ user: ubuntu,  duration: 20, aduration: 35, interval: 0, tool_cmd: \"argdist.py -C 't:syscalls:sys_exit_epoll_wait():u16:args->ret' -i 20 -d 20\", tool: sysprocess_exit_epoll_wait, ues: "$N_UES" }"
done
