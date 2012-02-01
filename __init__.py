import ConfigParser
import psutil
import subprocess

config_file='/home/navin/.ssh/config'

class BadProcess(Exception):
    pass

def restart(command, pidfile):
    command[0:0] = ['/usr/bin/env', 'daemonize', '-p', pidfile]
    subprocess.Popen(command)

def handle(program, command, pidfile, verifier, **kwargs):
    pidfile = pidfile.format(program=program)
    verifier = verifier.format(program=program)
    # replace {program} in pidfile/verifier name with actual program name
    command = command.split()

    try:
        pid = int(open(pidfile).read())
        p = psutil.Process(pid)
        pcmd = ' '.join(p.cmdline)
        if verifier not in pcmd:
            raise BadProcess(verifier + '::' + pcmd)
    except (IOError, psutil.NoSuchProcess, BadProcess):
        restart(command, pidfile)


def handle_all(config_file):
    c = ConfigParser.SafeConfigParser()
    c.read(config_file)

    for section in c.sections():
        handle(program=section,
               **dict((o, c.get(section, o)) for o in c.options(section)))


if __name__ == '__main__':
    handle_all('/tmp/config.cfg')

