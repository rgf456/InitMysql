import platform
import os
from Logo import print_logo, print_message
from subprocess import Popen, PIPE

mysqld = "[mysqld]"
client = "[client]"
mysql = "[mysql]"
server_charset = "character-set-server=utf8"
client_charset = "default-character-set=utf8"


def backup_original_file(file_object, data):
    print_message('back up your file to %s.bak_bak...' % file_object.name)
    f = open(file_object.name + '.bak_bak', 'w')
    name = f.name
    f.writelines(data)
    f.flush()
    f.close()
    print_message('back up your file success,you can open find it : %s' % name)


def replace_charset(file_object, data):
    if data.find(mysqld) < 0:
        backup_original_file(file_object, data)
        print_message("prepare write into file...")
        file_object.write(data)
        file_object.write('\n')
        file_object.write(mysqld)
        file_object.write('\n')
        file_object.writelines(server_charset)
        file_object.flush()
        print_message("write file success...")
    elif data.find(server_charset) < 0:
        backup_original_file(file_object, data)
        print_message("prepare write into file...")
        file_object.seek(0, 0)
        str = data.replace(mysqld, mysqld + '\n' + server_charset)
        file_object.writelines(str)
        file_object.flush()
        print_message("write file success...")
        print_message('you can restart your mysql...')
    else:
        print_message("you have already write server_char_set...")


def where_is_conf(create_file):
    filename = r'/etc/my.cnf'
    if os.path.exists(filename):
        print_message('find %s ,prepare to fix...' % filename)
        file_path = '/etc/my.cnf'
        correct(file_path)
    else:
        if create_file:
            file = '/etc/my.cnf'
            f = open(file, 'w')
            f.close()
            correct(file)


def correct(file_path):
    f = open(file_path, 'r+')
    try:
        all_text = f.read()
        replace_charset(f, all_text)
    finally:
        f.close()


def fix_ubuntu():
    file_path = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    correct(file_path)


def print_sys(sys_name):
    print_message('Your system is \"%s\" ' % sys_name)


# 判断平台，假如是osx，则会自动寻找/etc/my.cnf文件
def judge_platform():
    print_message('Looking for your System Version...')
    sys = platform.uname().version.lower()
    if sys.find('darwin') >= 0:
        print_sys('Darwin')
        where_is_conf(True)
    elif sys.find('ubuntu') >= 0:
        print_sys('Ubuntu')
        fix_ubuntu()
    elif sys.find('centos') >= 0:
        print_sys('CentOS')
        where_is_conf(True)
    else:
        print_message('Your system is %s,current not supported!!!' % platform.system())


def start_set_mysql_charset():
    print_logo()
    judge_platform()


start_set_mysql_charset()
