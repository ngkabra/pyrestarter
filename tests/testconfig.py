[DEFAULT]
dir = /tmp
rundir = %(dir)s/run
bindir = %(dir)s/bin
sbindir = %(dir)s/bin
pidfile = %(rundir)s/{program}.pid
verifier = {program}
daemonize_cmd = /usr/local/sbin/daemonize

[basic]
command = /bin/sh -c 'sleep 500 # verifier1'
verifier = verifier1

[basic_non_pid]
command = /bin/sh -c 'sleep 501 # verifier2'
verifier = verifier2
pidfile =

[basic_non_daemonize]
command = ssh -f sochle -L13079:localhost:13079 -N
daemonize = no
verifier = 13079
pidfile =
