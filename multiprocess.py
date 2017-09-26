# -*- coding:utf-8 -*-
from multiprocessing import Pool, Queue, Lock, SimpleQueue
import Queue
import os
import time
import random
import argparse

import utils

MAX_PROCESS = 5


def executor(name, r_queue):
    # print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    # print 'Task %s runs %0.2f seconds.' % (name, (end - start))
    r_queue.put('Task %s runs %0.2f seconds.' % (name, (end - start)))


def printer(r_name, r_count, r_queue, lock):
    """

    :param r_name:
    :param r_count:
    :param r_queue:
    :return:
    """
    i = 0
    while i < r_count:
        line = r_queue.get(True)
        if line:
            lock.acquire()
            print '[%d]' % (i + 1,),
            utils.print_output(line)
            lock.release()
            i += 1
        r_queue.task_done()


def main(r_parser):
    """
    :param r_parser: 传入的参数
    :return:
    """
    r_parser.add_argument("-m", "--module", help="module", required=True)
    r_parser.add_argument("-u", "--user", help="remote machine user", required=True)
    r_parser.add_argument("-p", "--password", help="remote machine password")
    r_parser.add_argument("-d", "--destination", help="destination hosts group", required=True)
    r_parser.add_argument("-c", "--command", help="command or shell scripts", required=True)
    args = r_parser.parse_args()
    module = args.module
    user = args.user
    password = args.password
    dest = args.destination
    command = args.command
    print 'Parent process %s.' % os.getpid()
    config = utils.read_config('./rcm.conf')
    hosts_lst = utils.get_hosts(config, dest)
    print hosts_lst
    _exe_command(hosts_lst, module, user, password, command)


def _exe_command(r_hosts_lst, r_module, r_user, r_password, r_command):
    """

    :param r_hosts_lst:
    :param r_module:
    :param r_user:
    :param r_password:
    :param r_command:
    :return:
    """
    queue = SimpleQueue()
    lock = Lock()
    p = Pool(MAX_PROCESS)
    # p.apply_async(printer, args=('printer', len(r_hosts_lst), queue))
    p.apply_async(printer, args=('printer', 5, queue, lock))
    for i in range(5):
        p.apply_async(executor, args=(i, queue))
    p.close()
    p.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''execute command or scripts on remote machine''')
    main(parser)