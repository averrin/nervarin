#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Fabric and boto based server admins tool
"""

"""
    TODO: evernote [http://habrahabr.ru/company/evernote/blog/57807/]
    TODO: more s3 bucket control (folder uploads, non public transfers)
"""

__author__ = "Alexey 'Averrin' Nabrodov <averrin@gmail.com>"
__version__ = '1.8.2'

#MODULES

try:
    from functools import partial
    from fabric.api import run, env, open_shell, put, sudo, local, parallel, lcd, cd
    from fabric.api import get as scp_get
    # from fabric.colors import red, green, cyan, yellow
    from fabulous.color import *
    from fabric.decorators import task
    import os
    import sys
    import shutil
    import json
    import boto
    from boto.s3.key import Key
    from jinja2 import Template
    import imp
    import urllib2
    from subprocess import *

except ImportError:
    print 'Plz install deps:'
    print '>\tsudo pip install fabric bottle boto jinja2 fabulous'
    exit(1)


def success(msg):
    s = bold(green(u' ✓  ') + msg)
    print s.as_utf8


def action(msg):
    s = cyan(u' >  ' + msg)
    print s.as_utf8


def error(msg):
    s = bold(red(u' ✘  ' + msg))
    print s.as_utf8


def info(msg):
    s = fg256('#eeee00', bold(u' !  ' + msg))
    print s.as_utf8


@task
def test():
    success('Servers saved on')
    error('Servers saved on')
    info('No local servers.json')

# CONFIG
USE_LOCAL = False
api_token = '3d714fb7-a389-4748-a781-2f9329fbc280'
PORT = 8080
serve_key = 'aqwersdf'
ssh_startup = 'TERM=xterm-256color tmux new-session -t default || TERM=xterm-256color tmux new-session -s default'
packages = ['git-core', 'tmux', 'zsh', 'curl', 'w3m', 'autojump', 'vim', 'wget', 'python-dev', 'htop']
pip_packages = ['supervisor', 'fabric', 'virtualenv']
pm_args = {'apt-get': '-ym --force-yes', 'yum': '-y'}
aliases = {'!': 'sudo', 'pipi': 'sudo pip install', 'p': "sudo python ~/p.py"}

cloud_files = [  # Must be public
    {'key': 'vimrc', 'path': '~/.vimrc', 'bucket': 'averrin'},
    {'key': 'p_py', 'path': '~/p.py', 'bucket': 'averrin'},
    ]

ssh_config = """
host bitbucket.org
user git
identityfile ~/.ssh/github"""

sync_repo = "git@bitbucket.org:anabrodov/sync.git"
projects_repo = "git@bitbucket.org:anabrodov/projects.git"

if os.path.basename(sys.argv[0]) == 'fab':
    home_folder = os.path.split(os.path.abspath(env['fabfile']))[0] + '/'
elif os.path.basename(sys.argv[0]) == 'ipython':
    home_folder = os.path.abspath('.')
else:
    home_folder = os.path.split(os.path.abspath(sys.argv[0]))[0] + '/'

remote_folder = '.'
central_server = '-i .temp/aws_ssh_averrin averrin@aws.averr.in'  # TODO: split to vars

servers_url = 'http://averrin.meteor.com/collectionapi/%s'

new_server = {
        "description": "",
        "tags": [],
        "ssh_port": 22,
        "ip": "",
        "host": "",
        "groups": ["ssh"],
        "projects": [],
        "ftp_port": 21,
        "other_hosts": [],
        "ssh_user": "averrin",
        "ssh_password": "",
        "ssh_cert": "",
        "os": "linux"
    }

# TODO: evernote tasks
evernote_key = 'averrin'
evernote_secret = '73dda0e225316788'

# ENDCONFIG


# SERVERS LOGIC
@task
def backup_json():
    """
        Backup servers on central server
    """
    if os.path.isfile(os.path.join(home_folder, 'servers.json')):
        action('Servers sending to remote server')
        put(os.path.join(home_folder, 'servers.json'), remote_folder)
        success('Servers saved on %s' % current()['alias'])


@task
def update_json():
    """
    Update servers from remote server
    """
    action('Servers getting from remote server')
    scp_get('servers.json', home_folder)
    success('Servers got from remote server')


class ServerList(dict):
    def __init__(self):
        self.load()
        self.certs = self.load_certs()
        self.by_tags = partial(self.by_attrs, 'tags')
        self.by_groups = partial(self.by_attrs, 'groups')
        self.by_projects = partial(self.by_attrs, 'projects')
        self.by_hosts = partial(self.by_attrs, 'other_hosts')
        success('Servers loaded')

    def by_attrs(self, key, *values):
        res = []
        for s in self.values():
            if len(set(values).intersection(s[key])) == len(values):
                res.append(s)
        return res

    def by_attr(self, key, value):
        res = []
        for s in self.values():
            if s[key] == value:
                res.append(s)
        return res

    @classmethod
    def getCert(cls, key):
        return cls.certs[key]

    def save(self):
        with file(os.path.join(home_folder, 'servers.json'), 'w') as f:
            f.write(json.dumps(self, indent=4))

    def load(self):
        if os.path.isfile(os.path.join(home_folder, 'servers.json')):
            action('Local servers.json existed')
            with file(os.path.join(home_folder, 'servers.json'), 'r') as f:
                self.update(json.loads(f.read()))
        else:
            info('No local servers.json')
            # execute(update_json, hosts=[central_server])
            # update_json()
            action('Servers getting from remote server')
            # os.system('scp %s:servers.json %s' % (central_server, home_folder))
            req = urllib2.Request(servers_url % 'SERVERS')
            req.add_header('X-Auth-Token', api_token)
            sc = urllib2.urlopen(req).read()
            if USE_LOCAL:
                with file(os.path.join(home_folder, 'servers.json'), 'w') as f:
                    f.write(sc)
                success('Servers got from remote server')
                self.load()
            else:
                ss = {}
                for s in json.loads(sc):
                    ss[s['alias']] = s
                self.update(ss)

    def load_certs(self):
        req = urllib2.Request(servers_url % 'KEYS')
        req.add_header('X-Auth-Token', api_token)
        sc = urllib2.urlopen(req).read()
        return json.loads(sc)


# ETC
def dump_to_file(filename, text, mod=777):
    with file(os.path.join(home_folder, '.temp/', filename), 'w') as f:
        f.write(text)
        os.system('chmod %s %s' % (mod, os.path.join(home_folder, '.temp/', filename)))
    return os.path.join(home_folder, '.temp/', filename)


def get_bucket(bucket):
    conn = boto.connect_s3(SERVERS['aws']['attrs']['aws_id'], SERVERS['aws']['attrs']['aws_key'])
    b = conn.get_bucket(bucket)
    return b


def get_s3_var(filename, bucket='averrin'):
    action('Servers getting file from S3')
    b = get_bucket(bucket)
    k = b.get_key(filename)
    success('Servers got %s from S3' % filename)
    return k.get_contents_as_string()


@task
def clean():
    """
        Clean temp files
    """
    os.system('chmod 777 -R %s' % os.path.join(home_folder, '.temp'))
    if os.path.isdir(os.path.join(home_folder, '.temp')):
        shutil.rmtree(os.path.join(home_folder, '.temp'))


def current():
    return SERVERS.by_attr('ip', env['host_string'].split('@')[1].split(':')[0])[0]


env.key_filename = []
clean()
os.mkdir(os.path.join(home_folder, '.temp'))
SERVERS = ServerList()
for cert in SERVERS.certs:
    env.key_filename.append(dump_to_file(cert['title'], cert['key'].replace('\\n', '\n'), 400))

for s in SERVERS:
    SERVERS[s]['alias'] = s

env.roledefs['linux'] = []
for s in SERVERS.by_attr('os', 'linux'):
    env.passwords['%(ssh_user)s@%(ip)s:%(ssh_port)s' % s] = s['ssh_password']
    s['host_string'] = '%(ssh_user)s@%(ip)s:%(ssh_port)s' % s
    env.passwords['%(ssh_user)s@%(host)s:%(ssh_port)s' % s] = s['ssh_password']
    for h in s['other_hosts']:
        env.passwords['%s@%s:%s' % (s['ssh_user'], h, s['ssh_port'])] = s['ssh_password']
    env.roledefs[s['alias']] = ['%(ssh_user)s@%(ip)s:%(ssh_port)s' % s]

for s in SERVERS.values():
    for g in s['groups']:
        if not g in env.roledefs:
            env.roledefs[g] = []
        if 'ssh_user' in s:
            env.roledefs[g].append('%(ssh_user)s@%(ip)s:%(ssh_port)s' % s)
        else:
            env.roledefs[g].append(s['ip'])


# FABRIC LOGIC
@task
def shell(native=False, tmux=True):
    """
        Open common ssh shell
    """
    if native or eval(str(native)):
        action('Opening native fabric shell')
        open_shell(ssh_startup if eval(str(tmux)) else '')
    else:
        action('Opening ssh shell')
        key = current()['ssh_cert']
        password = SERVERS.by_attr('ip', env['host_string'].split('@')[1].split(':')[0])[0]['ssh_password']
        if key:
            key = '-i ' + os.path.join(home_folder, '.temp/', key)
        ssh = "sshpass -p '%s' ssh %s -p %s %s %s" % (password,
            env['host_string'].split(':')[0],
            env['host_string'].split(':')[1],
            key,
            "-t '%s'" % ssh_startup if eval(str(tmux)) else '')
        os.system(ssh)
        print ssh
    clean()


@task
def send_file(local, remote):
    """
        Send file by scp
    """
    put(local, remote)
    # clean()


@task
def get_file(remote, local):
    """
        Send file by scp
    """
    scp_get(remote, local)
    # clean()


@task
def install(package):
    """
        Install package
    """
    pm = current().get('pm', 'apt-get')
    sudo('%s install %s %s' % (pm, package, pm_args[pm]))


@task
# @parallel
def init(full=False):
    """
        Install must-have tools like tmux, zsh and others
    """
    s = current()
    env.warn_only = True
    if eval(str(full)):
        action('Perfom full init')
        for p in packages:
            install(p)
        for p in pip_packages:
            pip(p)
        run('curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh')
    env.warn_only = False
    action('Renew configs')
    path = run('which zsh')
    put(dump_to_file('.tmux.conf', get_s3_var('tmux.conf').replace('{{shell}}', path)), '.')
    put(dump_to_file('.zshrc', Template(
        get_s3_var('zshrc')).render({'s': s,
            'aliases': aliases})), '.')
    for cf in cloud_files:
        run('wget "https://s3.amazonaws.com/%(bucket)s/%(key)s" -O %(path)s' % cf)
    run('git config --global user.email "averrin@gmail.com"')
    run('git config --global user.name "Alexey Nabrodov"')
    # clean()


@task
def get_info():
    """
        Get server info
    """
    action('Getting server info')
    import pprint
    # from pygments import highlight
    # from pygments.lexers import JSONLexer
    # from pygments.formatters import Terminal256Formatter
    # print green(u'>\t"%s" server info' % current()['alias'])
    # print highlight(pprint.pformat(current()), JSONLexer(), Terminal256Formatter())
    pprint.pprint(current())
    env.warn_only = True
    run('lsb_release -a', shell=False)
    run('uname -a', shell=False)
    run('uptime', shell=False)
    env.warn_only = False
    # clean()


@task
def full_backup():
    """
        Backup servers and this file on central server
    """
    action('Performing full backup')
    backup_json()
    action('Nervarin sending to remote server')
    put(env['fabfile'], remote_folder)
    success('Nervarin saved on %s' % current()['alias'])


@task
def pip(package):
    """
        Install python package
    """
    p = current().get('pip', 'pip')
    sudo('%s install %s' % (p, package))


# @hosts(SERVERS['aws']['host_string'])
# @task
# def aws_serve():
#     print env.hosts
#     run('daemon fab -f ~/nervarin.py serve')
#     local('curl "http://aws.averr.in:8080/search?q="')



@task
def edit_s3_file(filename, public=True, bucket='averrin'):
    b = get_bucket(bucket)
    k = b.get_key(filename)
    k.get_contents_to_file(file(os.path.join(home_folder, '.temp', filename), 'w'))
    os.system('vim %s' % os.path.join(home_folder, '.temp', filename))
    k.set_contents_from_file(file(os.path.join(home_folder, '.temp', filename), 'r'))
    if eval(str(public)):
        k.set_acl('public-read')


@task
def add_s3_file(filename, public=True, bucket='averrin'):
    b = get_bucket(bucket)
    k = Key(b)
    k.key = os.path.basename(filename)
    k.set_contents_from_file(file(filename, 'r'))
    if eval(str(public)):
        k.set_acl('public-read')


@task
def lsync():
    path = os.path.join(home_folder, 'sync')
    action('Run local sync')
    if not os.path.isdir(path):
        action('\tCloning sync repo')
        with lcd(home_folder):
            local('git clone %s' % sync_repo)
            success('tClonned. Do LS')
            local('ls ./sync')
    else:
        with lcd(path):
            action('\tPulling sync repo')
            local('git pull')
            s = local('git status -s', capture=True)
            if s:
                s = list(set([a if a[0] in 'AM' else None for a in s.split('\n')]))[-1]
                if s is not None:
                    info('\tHave changes, commiting')
                    local('git commit -am "sync"')
                    local('git push')
                    rsync()
    success('Local synced')


@task
def rsync():
    s = current()
    if 'sync' in s:
        action('Run remote sync')
        path = os.path.expanduser(s['sync'])
        if not eval(run('test -d %s && echo "True" || echo "False"' % path)):
            action('\tCloning sync repo')
            env.warn_only = True
            run('mkdir ~/.ssh')
            env.warn_only = False
            sudo('rm ~/.ssh/github')
            put(home_folder + '.temp/github', '~/.ssh/github')
            run('chmod 400 ~/.ssh/github')
            env.warn_only = True
            if not eval(run("test -f ~/.ssh/config && echo 'True' || echo 'False'")) or eval(run("cat ~/.ssh/config | grep 'bitbucket' >/dev/null && echo 'True' || echo 'False'")):
                run('echo "%s" >> ~/.ssh/config' % ssh_config)
            env.warn_only = False
            with cd(os.path.split(path)[0]):
                run('git clone %s %s' % (sync_repo, path))
            success('Clonned. Do LS')
            run('ls %s' % path)
            sudo('rm ~/.ssh/github')
        else:
            with cd(path):
                action('\tPulling sync repo')
                run('git pull')
                s = run('git status -s')
                if s:
                    s = list(set([a if a[0] in 'AM' else None for a in s.split('\n')]))[-1]
                    if s is not None:
                        info('\tHave changes, commiting')
                        run('git commit -am "sync"')
                        run('git push')
                        lsync()
        success('Remote synced')
    else:
        info('Sync not available for %s' % s['alias'])


@task
def sync():
    lsync()
    rsync()


# PROJECTS
def load_module(name, path):
    (file, pathname, description) = imp.find_module(name, [path])
    return imp.load_module(name, file, pathname, description)


def find_modules(path):
    modules = set()
    for filename in os.listdir(path):
        module = None
        if filename.endswith(".py"):
            module = filename[:-3]
        elif filename.endswith(".pyc"):
            module = filename[:-4]
        if module is not None:
            modules.add(module)
    return list(modules)


def load_projects():
    path = os.path.join(home_folder, 'projects')
    if not os.path.isdir(path):
        with lcd(home_folder):
            local('git clone %s' % projects_repo)
    else:
        with lcd(home_folder):
            local('git pull')
    sys.path.append(path)
    from base import Project
    projects = {}
    _modules = [load_module(name, path) for name in find_modules(path)]

    for module in _modules:
        for obj in module.__dict__.values():
            try:
                if issubclass(obj, Project):
                    projects[obj.definition['title']] = obj
            except TypeError:
                pass
    return projects


def get_project(project_name, **kwargs):
    return load_projects()[project_name](home_folder=home_folder, **kwargs)


@task
def install_project(project_name, **kwargs):
    action('Installing project "%s"' % project_name)
    project = get_project(project_name, **kwargs)
    project.install()
    project.start()
    if project.check():
        success('Project "%s" installed' % project_name)
    else:
        error('Check failed=(')


@task
def check_project(project_name):
    action('Checking project "%s"' % project_name)
    project = get_project(project_name)
    if project.check():
        success('Project "%s" installed' % project_name)
    else:
        error('Check failed=(')



@task
def list(ping=False):
    pings = []
    for s in SERVERS.values():
        # if 'noping' not in s or not s['noping']:
        p = {}
        # print s['ip']
        p['addr'] = blue(bold(' >  ')) +\
            bold(s['alias']) +\
            blue(bold(u' — %(description)s [' % s)) +\
            bold(green(s['ip'])) +\
            bold(blue(']'))
        if 'noping' not in s or not s['noping']:
            p['ping'] = Popen(['ping', s['ip'], '-c', '2'], stdout=PIPE, stderr=PIPE)
        pings.append(p)
    if eval(str(ping)):
        action('Ping servers')
        for s in pings:
            print s['addr'].as_utf8
            if 'ping' in s:
                c = s['ping'].communicate()[0]
                if c and c.find('100% packet loss') == -1:
                    success('Online')
                else:
                    info('Offline')
            print
    else:
        for s in pings:
            print s['addr'].as_utf8



if __name__ == "__main__":
    os.system('ipython --quick -c "import nervarin as n" -i')
