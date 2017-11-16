# -*- coding:utf-8 -*-

"""
utilitis function or method
"""

import os
import sys
import re
import logging
import time

G_LOGGER_INS_NAME = 'remote_shell'


def read_config(r_config_file):
    """
    :param r_config_file: 配置文件
    :return:
    """
    if not os.path.exists(r_config_file):
        print "config file %s not exists" % (r_config_file,)
        sys.exit(1)
    with open(r_config_file) as handle:
        lines = handle.readlines()

    ret_rst = {}
    key = ''
    for line in lines:
        line = line.strip('\n\r')
        line = _strip_comment(line)
        if not line:
            continue
        if line.startswith('['):
            key = line[1:-1]
        else:
            lst = ret_rst.get(key, [])
            lst.append(line)
            ret_rst[key] = lst

    return ret_rst


def _strip_comment(r_line):
    """
    去掉注释
    :param r_line:
    :return:
    """
    if r_line.startswith('#'):
        return None
    index = r_line.find('#')
    if index > 1:
        line = r_line[:index]
        line = line.strip(' ')
    else:
        line = r_line

    return line


def print_output(r_lst):
    """
    打印命令行输出的内容
    :param r_lst:
    :return:
    """
    for line in r_lst:
        print line


def get_hosts(r_config, r_dest):
    """
    :param r_config: 主机组配置[dir]
    :param r_dest: 目标主机组 [str]
    :return: [list]
    """
    matched_str = []
    rst = []

    for key in r_config.keys():
        if re.match(r_dest, key):
            matched_str.append(key)

    for key in matched_str:
        rst += r_config.get(key)

    # print rst
    return rst


def red_font(r_str):
    """
    显示红字
    :param r_str:
    :return:
    """
    return "%s[31;2m%s%s[0m" % (chr(27), r_str, chr(27))


def green_font(r_str):
    """
    显示绿字
    :param r_str:
    :return:
    """
    return "%s[32;2m%s%s[0m" % (chr(27), r_str, chr(27))


def split_copy_command(r_str):
    """
    'src = /abc/123/a.txt dest=/def/user/' => ['/abc/123/a.txt', '/def/user/']
    :param r_str: [str]
    :return: [list]
    """
    t_lst = re.split('=| ', r_str)
    lst = []
    for t_str in t_lst:
        if t_str not in ['src', '', 'dest']:
            lst.append(t_str)

    return lst


def get_logger(console=False):
    """
    :return:
    """
    logger = logging.getLogger(G_LOGGER_INS_NAME)
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.ERROR)
    date_str = time.strftime("%Y%m%d", time.localtime(time.time()))
    file_name = '%s_remote_shell.log' % (date_str,)
    log_file = os.path.expandvars('./log/' + file_name)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s--%(name)s--%(levelname)s--%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        pass
        # logger.info('foorbar')

    return logger


if __name__ == '__main__':
    print read_config('./rcm.conf')
