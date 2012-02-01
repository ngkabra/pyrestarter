import ConfigParser
import psutil
import subprocess

class BadProcess(Exception):
    pass

def restart(command, pidfile, chdir, dry_run=False):
    daemonize = ['/usr/bin/env', 'daemonize', '-p', pidfile]
    if chdir:
        daemonize.extend(['-c', chdir])

    command[0:0] = daemonize
    if not dry_run:
        subprocess.Popen(command)
    else:
        print 'Re-Start:', command

def handle(program, command, pidfile, verifier,
           dry_run=False,
           **kwargs):
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
        restart(command, pidfile, kwargs.get('chdir'), dry_run=dry_run)


def handle_all(config_file, dry_run=False):
    c = ConfigParser.SafeConfigParser()
    c.read(config_file)

    for section in c.sections():
        handle(program=section,
               dry_run=dry_run,
               **dict((o, c.get(section, o)) for o in c.options(section)))


if __name__ == '__main__':
    import argparse
    from os.path import expanduser, exists
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', default='~/pyrestarter.cfg')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False)
    args = parser.parse_args()
    config_file = expanduser(args.config_file)
    if not exists(config_file):
        print 'No such file {0}'.format(config_file)
        exit(1)
    handle_all(config_file, dry_run=args.dry_run)
