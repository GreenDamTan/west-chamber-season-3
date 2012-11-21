#!/bin/sh +x

case "$1" in
    start)
        for i in `seq 1 89`; do
        python dos.py &
        done 
        ;;

    stop)
        ps axu|grep dos|grep -v "grep"|awk '{print $2}'|xargs -L1 kill
        ;;

    restart)
       	$0 stop
        $0 start
        ;;
    status)
        ps axu|grep dos|grep -v "grep"|wc |awk '{print $1" running processes"}'
        ;;
   *)
        echo "Usage: $0 {start|stop|restart|status}"
        ;;

esac
