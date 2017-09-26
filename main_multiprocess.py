# -*- coding:utf-8 -*-
"""
execute command or shell scripts on remote machine
multi process version
"""
import argparse
import multiprocessing
import Queue
import time

import pexpect
from pexpect import pxssh

import utils

# THREAD_LOCK = threading.Lock()


class Executor(multiprocessing.Process):
    """
    执行远程命令
    """

    def __init__(self, queue, name, host, user, password, command, module, port=22):
        # super(Executor, self).__init__()
        multiprocessing.Process.__init__(self)
        self.name = name
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.command = command
        self.queue = queue
        self.module = module

    def run(self):
        """
        :return:
        """
        if self.module == 'command':
            self.exec_command()
        elif self.module == 'copy':
            self.exec_copy()
        elif self.module == 'shell':
            self.exec_copy()

        return

    def exec_command(self):
        """
        :return:
        """
        t_res = self.auto_ssh(self.user, self.password, self.host, [self.command])
        t_res = self.reunit_res(t_res)
        t_res.insert(0, utils.green_font('=' * 10 + self.host + '=' * 10 + 'success'))
        # THREAD_LOCK.acquire()
        # self.queue.put(
        #         '%s-%s-%s-%s' % (self.host, self.user, self.password, self.command))
        self.queue.put(t_res)
        # THREAD_LOCK.release()

    def exec_copy(self):
        """
        :return:
        """
        t_lst = utils.split_copy_command(self.command)
        src_file = t_lst[0]
        remote_path = t_lst[1]
        t_res = self.scp_file(self.user, self.host, remote_path, src_file, self.password)

        lst = []
        if t_res:
            lst.append(utils.green_font('=' * 10 + self.host + '=' * 10 + 'success'))
            # THREAD_LOCK.acquire()
            self.queue.put(lst)
            # THREAD_LOCK.release()
        else:
            lst.append(utils.red_font('=' * 10 + self.host + '=' * 10 + 'fail'))
            # THREAD_LOCK.acquire()
            self.queue.put(lst)
            # THREAD_LOCK.release()

    def reunit_res(self, r_res):
        """
        :param r_res:
        :return:
        """
        res = list()
        for i in r_res[0].split('\r\n'):
            res.append(i)

        return res

    def auto_ssh(self, r_user, r_passwd, r_host, r_cmd_list):
        """
        :param r_user:
        :param r_passwd:
        :param r_host:
        :param r_cmd_list:
        :return:
        """
        result = list()

        try:
            ssh = pxssh.pxssh()
            ssh.login(r_host, r_user, r_passwd, login_timeout=4)
            for cmd in r_cmd_list:
                ssh.sendline(cmd)
                ssh.prompt()
                # print ssh.before
                result.append(ssh.before)
            ssh.logout()
        except pxssh.ExceptionPxssh, e:
            print 'pxssh failed to login' + ':' + r_host
            print 'exception info: %s' % (str(e))
            # self.logger.error('exception info: %s' % (str(e),)
            return result

        return result

    def scp_file(self, r_user, r_ip, r_remote_path, r_file, r_passwd):
        """
        将当前主机的文件拷贝到远程主机的目录下
        :param r_user: 远程主机用户名
        :param r_ip: 远程主机ip
        :param r_remote_path: 远程主机路径
        :param r_file: 当期主机文件
        :param r_passwd: 远程主机密码
        :return:
        """
        print 'scp %s %s@%s:%s' % (r_file, r_user, r_ip, r_remote_path)
        child = pexpect.spawn('scp %s %s@%s:%s' % (r_file, r_user, r_ip, r_remote_path))
        try:
            child.expect('password: ', timeout=2)
        except pexpect.TIMEOUT:
            print 'time out'
            return False
        except pexpect.EOF:
            return True
        child.sendline('%s' % r_passwd)
        time.sleep(.2)
        # print 'success'
        return True


class Printer(multiprocessing.Process):
    """
    打印输出
    """

    def __init__(self, r_name, r_count, r_queue):
        """
        :param r_name:
        :param r_count:
        :param r_queue:
        :return:
        """
        # super(Printer, self).__init__()
        multiprocessing.Process.__init__(self)
        self.name = r_name
        self.count = r_count
        self.queue = r_queue

    def run(self):
        """
        :return:
        """
        i = 0
        while i < self.count:
            line = self.queue.get(True)
            if line:
                print '[%d]' % (i + 1,),
                utils.print_output(line)
                i += 1
            self.queue.task_done()

        return


def _exe_command(r_hosts_lst, r_module, r_user, r_password, r_command):
    """
    :param r_hosts_lst:
    :param r_module:
    :param r_user:
    :param r_password:
    :param r_command:
    :return:
    """
    thread_lst = []
    queue = Queue.Queue()

    p_thread = Printer('printer', len(r_hosts_lst), queue)
    # p_thread.start()
    thread_lst.append(p_thread)
    p_thread.start()
    for host in r_hosts_lst:
        thread = Executor(queue, 'thread:%s' % (host,), host, r_user, r_password, r_command, r_module)
        thread_lst.append(thread)
        thread.start()

    for thread in thread_lst:
        thread.join()

        # while queue.qsize() != 0:
        #     # print queue.get(True)
        #     utils.print_output(queue.get(True))


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
    config = utils.read_config('./rcm.conf')
    hosts_lst = utils.get_hosts(config, dest)
    _exe_command(hosts_lst, module, user, password, command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''execute command or scripts on remote machine''')
    # parser.add_argument("-m", "--module", help="module", required=True)
    main(parser)
