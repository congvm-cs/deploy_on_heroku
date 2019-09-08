DAEMON_PATH=$(pwd)
CONF_FILE=$DAEMON_PATH/run_flask_app.py
LOG_FILE=$DAEMON_PATH/logs/run_flask_app.log

# DAEMON=$(which python3)
DAEMON=/home/congvm/.virtualenvs/dl-py3/bin/python3
DAEMONOPTS="-u $CONF_FILE"

NAME=run_flask_app
SERVICE=run_flask_app
DESC="run_flask_app"
PIDFILE=$DAEMON_PATH/pid/$SERVICE.pid


case "$1" in
start)
	printf "%-50s" "Starting $NAME..."
	cd $DAEMON_PATH
	#PID=`$DAEMON $DAEMONOPTS > /dev/null 2>&1 & echo $!`
	$DAEMON $DAEMONOPTS > $LOG_FILE 2>&1 &
	PID=`echo -n $!`
	#echo "Saving PID" $PID " to " $PIDFILE
        if [ -z $PID ]; then
            printf "%s\n" "Fail"
        else
            echo $PID > $PIDFILE
            printf "%s\n" "Ok"
        fi
;;
status)
        printf "%-50s" "Checking $NAME..."
        if [ -f $PIDFILE ]; then
            PID=`cat $PIDFILE`
            if [ -z "`ps axf | grep ${PID} | grep -v grep`" ]; then
                printf "%s\n" "Process dead but pidfile exists"
            else
                echo "Running"
            fi
        else
            printf "%s\n" "Service not running"
        fi
;;
stop)
        printf "%-50s" "Stopping $NAME"
            PID=`cat $PIDFILE`
            cd $DAEMON_PATH
        if [ -f $PIDFILE ]; then
            kill -HUP $PID
            printf "%s\n" "Ok"
            rm -f $PIDFILE
        else
            printf "%s\n" "pidfile not found"
        fi
;;

restart)
  	$0 stop
  	$0 start
;;

*)
        echo "Usage: $0 {status|start|stop|restart}"
        exit 1
esac