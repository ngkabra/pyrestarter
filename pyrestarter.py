import logging
logger = logging.getLogger(__name__)


import ConfigParser
import psutil
import subprocess


class PyRestarterError(Exception):
    pass


class VerifierFailed(PyRestarterError):
    pass


class MultipleProcessesFound(PyRestarterError):
    pass


def restart(command, pidfile, chdir, dry_run=False,
            daemonize_cmd=None, daemonize=''):
    if daemonize.lower() not in ('no', 'false'):
        if daemonize_cmd:
            dcmd = daemonize_cmd
        else:
            dcmd = '/usr/bin/env daemonize'

        if pidfile:
            dcmd += ' -p ' + pidfile

        if chdir:
            dcmd += ' -c ' + chdir
        command = dcmd + ' ' + command

    if not dry_run:
        logger.debug('Run cmd: {}'.format(command))
        subprocess.check_call(command, shell=True)
    else:
        print '(Re-)Start:', command

def find_program(pidfile, verifier):
    '''Return the psutil.Process if process is running, else None'''
    if pidfile:
        try:
            pid = int(open(pidfile).read())
            p = psutil.Process(pid)
            pcmd = ' '.join(p.cmdline())
            if verifier not in pcmd:
                raise VerifierFailed(verifier + '::' + pcmd)
            else:
                return p
        except (IOError, psutil.NoSuchProcess, VerifierFailed):
            return None
    else:
        # directly use verifier
        matches = []
        for pid in psutil.get_pid_list():
            try:
                p = psutil.Process(pid)
            except psutil.error.NoSuchPress:
                pass
            pcmd = ' '.join(p.cmdline())
            if verifier in pcmd:
                matches.append(p)
        if len(matches) == 2:
            raise MultipleProcessesFound('{}: Skipping'.format(verifier))
        elif len(matches) == 0:
            return None
        else:
            return matches[0]


def handle(program, command, pidfile, verifier,
           dry_run=False,
           force_restart=False,
           kill_program=False,
           show_status=False,
           **kwargs):
    if kwargs.get('skip', '').lower() in ('true', 'yes'):
        logger.debug('Skipping ' + program)
        return
    else:
        logger.debug('Handling ' + program)

    pidfile = pidfile.format(program=program)
    verifier = verifier.format(program=program)
        # replace {program} in pidfile/verifier name with actual program name

    if not pidfile and not verifier:
        logger.debug('{}: pidfile and verifier are none. Skipping'.format(
            program))

    process = find_program(pidfile, verifier)
    if force_restart or kill_program:
        if process:
            logger.debug('Found process {} - killing'.format(program))
            if not dry_run:
                process.kill()
            else:
                print 'Kill: ', process
        else:
            logger.debug('Process {} is not running'.format(program))
        if kill_program:
            return                        # do not restart it
        do_restart = True
    else:
        do_restart = not process

    if show_status:
        print '{} is {}running'.format(program,
                                        'NOT ' if do_restart else '')
    elif do_restart:
        logger.debug('Restarting ' + program)
        restart(command, pidfile, kwargs.get('chdir'),
                dry_run=dry_run,
                daemonize_cmd=kwargs.get('daemonize_cmd'),
                daemonize=kwargs.get('daemonize', ''))
    else:
        logger.debug('Already running {} pid={}'.format(program, process.pid))


def handle_all(config_file, dry_run=False,
               force_restart=None,
               kill_program=None,
               kill_all=False,
               show_status=False):
    c = ConfigParser.SafeConfigParser()
    c.read(config_file)

    if force_restart or kill_program:
        progname = force_restart or kill_program
        if progname in c.sections():
            sections = [progname]
        else:
            logger.debug('program {} not found in cfg file'.format(
                progname))
            return
    else:
        sections = c.sections()


    for section in sections:
        handle(program=section,
               dry_run=dry_run,
               force_restart=force_restart,
               kill_program=kill_program or kill_all,
               show_status=show_status,
               **dict((o, c.get(section, o)) for o in c.options(section)))


if __name__ == '__main__':
    import argparse
    from os.path import expanduser, exists
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', default='~/pyrestarter.cfg')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False)
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    parser.add_argument('-r', '--restart', help='Force restart of program')
    parser.add_argument('-k', '--kill', help='Kill program')
    parser.add_argument('-K', '--Killall', action='store_true',
                        help='Kill all programs')
    parser.add_argument('-s', '--status', action='store_true',
                        help='Show status of all programs')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    logger.debug('Started pyrestarter')
    config_file = expanduser(args.config_file)
    if not exists(config_file):
        print 'No such file {0}'.format(config_file)
        exit(1)

    handle_all(config_file,
               dry_run=args.dry_run,
               force_restart=args.restart,
               kill_program=args.kill,
               show_status=args.status,
               kill_all=args.Killall,
        )
