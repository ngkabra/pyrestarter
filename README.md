__This is probably not production ready yet__

An auto-restarter script that reads a config file containing commands and PID file names, checks whether the processes are still running, and restarts them if they are not. Suitable for putting in cron. Requires [daemonize](http://software.clapper.org/daemonize/)

supervisord is too heavyweight. init.d and friends are too shell-scripty, and most expect root permissions.

See example_pyrestarter.cfg and tests/testconfig.cfg for examples. Here only rundir and pidfile are necesary. The other settings are there for your convenience.

### Usage

Install daemonize. pyrestarter.py uses daemonize to put your command in the background.

Create a pyrestarter.cfg in your home directory, and configure 'rundir' and 'daemonize_cmd'. Make sure the 'rundir' directory exists and is writable by pyrestarter.py. Then in your cron, put:

     * * * * * /usr/bin/python /path/to/pyrestarter.py

Or if you dont want to put pyrestarter.cfg in your home directory you can do:

       ...pyrestarter.py -c somedir/somefile.cfg

From the command line you can do the following:

       $ pyrestarter.py -s
         # shows current running status of programs listed in the cfg file
       $ pyrestarter.py -k <progname>
         # kill <progname> - where <progname> is the program name as
         # as defined in the cfg file (the part between [square_brackets])
       $ pyrestarter.py -r <progname>
         # kill and restart <progname>
