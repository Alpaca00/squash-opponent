import os
import sys
import time
from loguru import logger
import paramiko
import argparse


logger.add(
        sys.stderr, format="{time} {level} {message}", filter="my_module", level="CRITICAL"
    )
SSH_PASSWORD = os.environ["SSH_PASSWORD"]

arg = argparse.ArgumentParser()
arg.add_argument("-u", dest="upload", action="store_true", help="upload log file")
arg.add_argument("-l", dest="logs", action="store_true", help="read logs")
arg.add_argument("-с", dest="containers", action="store_true", help="show containers")
args = arg.parse_args()


def main(args):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname='46.101.139.62', username='root', password=SSH_PASSWORD, port=22, timeout=5)
    try:
        stdin, stdout, stderr = client.exec_command('docker --version', get_pty=True)
        if "Docker version 20.10.7, build f0df350" in stdout.read().decode('utf-8'):
            if args.containers:
                stdin, stdout, stderr = client.exec_command("docker ps | sed -n '2,$p' |awk '{print $1}'")
                con_id_list = stdout.readlines()
                print(con_id_list)
            if args.logs:
                stdin, stdout, stderr = client.exec_command(f'docker logs 90cd5fc0a561 >> outlogs')
                stdin, stdout, stderr = client.exec_command('cat outlogs')
                logs = stdout.read()
                print(logs.decode('utf-8'))
            if args.upload:
                sftp = client.open_sftp()
                sftp.get('/root/outlogs', '/home/oleg/python/alpaca_web/tests/logs/outlogs')
    except Exception as err:
        logger.critical(err)
    time.sleep(5)
    client.close()


if __name__ == "__main__":
    main(args)
