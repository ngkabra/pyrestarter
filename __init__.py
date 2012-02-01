import ConfigParser
import psutil
import subprocess

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
    import argparse
    from os.path import expanduser, exists
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', default='~/pyrestarter.cfg')
    args = parser.parse_args()
    config_file = expanduser(args.config_file)
    if not exists(config_file):
        print 'No such file {0}'.format(config_file)
        exit(1)
    handle_all(config_file)
