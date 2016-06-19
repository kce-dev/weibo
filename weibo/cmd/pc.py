#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2016
# author: zwei
'''
Crawler same weibo info
'''
import os
import sys
import argparse

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir,
                               "weibo",
                               "__init__.py")):
    sys.path.insert(0, possible_topdir)

import weibo
from weibo import simu
from weibo import version
from weibo import userdata
from weibo import exception
from weibo.api import api
from weibo.db import migration
from weibo.common import cfg
from weibo.common import log

CONF = cfg.CONF
import pdb;pdb
dev_conf = os.path.join(possible_topdir,
                        'etc',
                        'weibo.conf')

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.
        """
        self.print_usage(sys.stderr)
        #FIXME(lzyeval): if changes occur in argparse.ArgParser._check_value
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, "error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                  " for more information.\n" %
                  {'errmsg': message.split(choose_from)[0],
                   'mainp': progparts[0],
                   'subp': progparts[2]})


def config_file(prog='weibo', description=None):
    _oparser = ArgumentParser(prog=prog,
                               description=description,
                               add_help=False,
                               epilog='See "weibo help subcommand" '
                               'for help on a specific command.',
                              )
    _oparser.add_argument('-h', '--help',
                          action='store_true',
                          help=argparse.SUPPRESS)

    _oparser.add_argument('-V', '--version',
                          action='version',
                          version=version.VERSION,
                         )

    _oparser.add_argument('-d', '--debug',
                          action='store_true',
                          help="Print debugging output")

    _oparser.add_argument('--config-file',
                          nargs='?',
                          help='Path to a config file to use. Multiple config '
                          'files can be specified, with values in later '
                          'files taking precedence. The default files ',
                         )
    _oparser.add_argument('--config_file',
                          help=argparse.SUPPRESS,
                         )
    return _oparser.parse_args()

args = config_file()

if os.path.exists(dev_conf):
    CONF(dev_conf)
    # LOG = logging.setup(*argv[:-1])
else:
    if args.config_file:
        if os.path.exists(args.config_file):
            CONF(args.config_file)
        else:
            CONF()
    else:
        CONF()


def db_sync(version=None):
    """Sync the database up to the most recent version."""
    return migration.db_sync(version)


def db_version(self):
    """Print the current database version."""
    print migration.db_version()


def client():
    # API 参考 http://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI
    # 使用参考 https://github.com/lxyu/weibo
    #useapi = api.useAPI()
    udata = userdata.Userdata()
    udata.save_all_users()
    #print(useapi.get('users/show', screen_name="海涛法师"))
    # print(api.get('statuses/user_timeline'))
    # print(api.get('statuses/user_timeline/ids'))
    #print(useapi.get('statuses/queryid', mid="1035051413304027"))
    # print(api.post('statuses/update', status='test from my api'))


def login():
    # 首先登入
    simu.Simu.check_login()

    # 模拟登陆的功能扩展待完善
    simulogin = simu.Simu()

    try:
        simulogin.detail()
    except exception.DetailNotFound:
        simu.Simu.reset_login()
        simulogin = simu.Simu()
        simulogin.detail()

    simulogin.save_all_data()
    # print(simulogin.detail('http://weibo.com/kaifulee'))


def pweibo():
    config_file()

def pmain():
    login()

def amain():
    client()

def dbmain():
    db_sync()


if __name__ == '__main__':
    dbmain()
