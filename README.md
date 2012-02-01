__You probably don't want to use this.__

An auto-restarter script that reads a config file containing commands and PID file names, checks whether the processes are still running, and restarts them if they are not. Suitable for putting in cron. Requires [daemonize](http://software.clapper.org/daemonize/)

supervisord is too heavyweight.
init.d and friends are too shell-scripty, and most expect root permissions.

