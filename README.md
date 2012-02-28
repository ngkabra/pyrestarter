__You probably don't want to use this.__

An auto-restarter script that reads a config file containing commands and PID file names, checks whether the processes are still running, and restarts them if they are not. Suitable for putting in cron. Requires [daemonize](http://software.clapper.org/daemonize/)

supervisord is too heavyweight. init.d and friends are too shell-scripty, and most expect root permissions.

See example_pyrestarter.cfg for examples. Here only rundir and pidfile are necesary. The other settings are there for your convenience.

### Usage

Install daemonize and ensure that it is in the path. pyrestarter.py uses daemonize to put your command in the background.

Create a pyrestarter.cfg in your home directory, and configure 'rundir. Make sure the 'rundir' directory exists and is writable by pyrestarter.py. Then put:

       pyrestarter.py

in your cron. Or you can do

       pyrestarter.py -c somedir/somefile.cfg
