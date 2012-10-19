#!/usr/bin/env python
# -*- coding: utf-8 -*-

#MODULES

try:
    from functools import partial
    from fabric.api import run, env, open_shell, put, sudo, local, parallel
    from fabric.api import get as scp_get
    # from fabric.api import puts as fabprint
    from fabric.colors import red, green, cyan, yellow
    from fabric.decorators import task, hosts
    # from fabric.tasks import execute
    import os
    import sys
    import shutil
    import json
    import boto
    from boto.s3.key import Key
except ImportError:
    print 'Plz install deps:'
    print '>\tsudo pip install fabric bottle boto'
    exit(1)


# CONFIG
PORT = 8080
serve_key = 'aqwersdf'
ssh_startup = 'TERM=xterm-256color tmux new-session -t default || TERM=xterm-256color tmux new-session -s default'
packages = ['tmux', 'zsh', 'curl', 'w3m', 'autojump', 'vim']
pip_packages = ['supervisor', 'fabric', 'virtualenv']
pm_args = {'apt-get': '-ym --force-yes', 'yum': '-y'}
aliases = {'!': 'sudo', 'pipi': 'sudo pip install'}

cloud_files = [
    {'key': 'vimrc', 'path': '~/.vimrc', 'bucket': 'averrin'},
    ]

if os.path.basename(sys.argv[0]) == 'fab':
    home_folder = os.path.split(os.path.abspath(env['fabfile']))[0] + '/'
elif os.path.basename(sys.argv[0]) == 'ipython':
    home_folder = os.path.abspath('.')
else:
    home_folder = os.path.split(os.path.abspath(sys.argv[0]))[0] + '/'

remote_folder = '.'
central_server = '-i .temp/aws_ssh_averrin averrin@aws.averr.in'
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

# ENDCONFIG


certs = {'aws_ssh_averrin': """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAq+moeI+se2KY00Z8FEL1cupE71y7Kvn1hkfUwX7gsg2YiAZY
0TqJ0D784o5/kkaaYNbqPzNbey5ZtdRK6R0Yk3OhxQfG+bJq+PGrcr10q5pSq3uI
FXRX5dB0IWh49+L/LFmu8bWKsbmPkFsE2jakROxXSJiflMnAAbzp1Ep57YFkGmJ+
/UY9Jf7M1UT/om/KLx8CJIqKEUjiIpWwo6D/NUif7JZ8P6H5P4nxeJHQDr7giuf+
Cs7RpI7OpWWgf6bBfY9ASPengg/KKgHfUiYlOKQFjH1kT+T+hnIVmQsRanC9xm8c
ldoF7TxMenRmZ7jZBIDCxwIstXvZ2plf3txtjwIDAQABAoIBAAn91ZXUO+Eb9Ofq
o9GFpsBcD0+eIx63UmbQi/QHDMYsdh4JyGW4skPRNV9xisaUpepU815i/MEnC32+
7e+oikIfqVpLPmxKy17WpPFRQ5Opr35Z+qnMjkNEH0vFx6oYnl4UhE92Dq6Pq2Fn
eNu560g6OER24meCZk9zjF+TSIzeLNyVG3fXaJgJlyDKnMrf6aH11fm52lhI8Iw7
Sl7R9HYOF0/A/HWJvUwrJmIkH1H4AMKOD+h+xD4g8Ck071G/sebgdbkuseUm/idP
BEFj1nl6HgO9oLPQWhwawDDxVBGNA0K7mmseYfOWocGqw+H90zaKdR6p6VAmzaOL
wbgKdGECgYEA465ZxeMXQaGtD3IEDCBpdqgFpULfRqEFT8Mxb87ua8MU56+BkGSj
pc3J9cULcgRp1AiO3DTEw4iO7t1LtwI88BRTdTGUY5jfCuuuQQFb1+Wk+yDWiFmj
YN8fYn3/9O7yqTRlGq4JDPDPyvrnRXILFJzdYhcLqMslJqSXiV77xl8CgYEAwUuS
+BSuP15EODh1eDaiwVsuEUzyTICk1bRsE4Y+FVxjnX/vVkeXGoY3+1h9VI7HqKp7
6lnbw/wQHoubQSbqAm91r/Z+jAlkJD0a/YYUtjd3yF0GMwkSPQsSKKzaP9eyt8WH
0B9G/MBvGpSv5/uLranch0HfQzBLsRqgXd9extECgYAZKpBpuyw66PAEIQopfPur
Te8x0S501B+OLXktbqYT60BIS7H6j+U20oRcUidttucrtLZ1yK9nHZUO+g8Ab5Lk
xppi/dP1HlSpFFvye3/3YT7XM04DTEUu0/rYHC1KmY7g/RWf2VTOxV9yhEFD/9MR
uDUQPpPfWHUGzHKjkIgr6QKBgQClP9LZu/RrwE9aMQpcR3lFDIqJx9qthJ1nBeQP
nQiegmm3UJRwkqufxXc+rhwXmikfDQD7DO9Q0cGGG5wTSw1sH5XhZT4ywiSWxpa4
f1Rdo3YIGV8fanXpMfnIRF4hjmn/qiO9zb+GfY1+j/cCwI5dXYZnK+2PJ07OjhDj
r/76wQKBgDCW4Sm8wWY50mF9T+FbHfQF7pTTPaJFWXFx2Zw01K2DErng1CeSFR2H
t75boytqJbcb4LLn6Yc/MVHjisXqGC6vQzTLeqXacahzzYSp2zYR1TN9VM1CZVHM
12XZZHD96R6wTIbb1kVQ8wretpUhDm/6TGAznMBYF2r2kUY4AEdg
-----END RSA PRIVATE KEY-----""",
    'aws_key': """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJTX7G9vKhMVdx+GlR9OZA+k+U1y
6w3ZYUH1zfD14j+z4/TJnpvG5qMXMDtjrTnJO2HbCL1i+SJHGIzhqUD/7YbCuJuKL7x8H0/Ser1X
gdCNcMu3YbEkxBFUkIhqpBHalrGq/Zm+jDaCKtaD0M7Zv4zC4W5/mCtBtwA/1Hki+cVVAgMBAAEC
gYBO63Is37diaQZBi/1znQAHH4UkYKNrM3CTJb7tXaJ5/msG9wSHOl496WSkiMRnmGBJEXc/28OX
PjUxNdGlak3JUBL3TOy2EkVOZ4wvr2uVWPUlTqXfQRydmM72A7H3rmkv8EmdIjxb+0WAtDNuS+Rl
Cd8Kl4MPMQmQnKMhNNV9wQJBAM459oM0c+swE5a3U9tUsX40Vq9rK3ywPX386CIIHNA1QJYnksGp
ZhTy8wQtKAdzr2kE4baZEuJe7pbnNWYzNbECQQC4xHXGf0IPpWtNlH05dwtxuxxXAsY6vjWAPqIK
HxbQ5V6YAslsA+2B4wqvvPnkBh7jDwxSFDntz6eWLAp84B7lAkEArT4WL4yN4MJHgnJJuNRCMyIm
vECMjLfFQKSIIaatBd/mfP2LlLMI9YpOynBg0znE3rViJDIdohtb1VswCcX1UQJANE8acNnyX++b
E1mooi47xTUN7uxQJq1XBDm3Mlpe4UEuqKaRU81A3nbivaIotQ+uiuXlvQ8Q32zcqz1IstXYqQJA
Q8iG/FHuVOVc2IZkx8hHMvaRP8EP7R2RMArA5yW//XJtLwCp51oJ7NDH0PTXPzzcJTcFQzKDkD0n
zBr5MFanRw==
-----END PRIVATE KEY-----""",
    'aws_cert': """-----BEGIN CERTIFICATE-----
MIICdzCCAeCgAwIBAgIGAIrPIWKZMA0GCSqGSIb3DQEBBQUAMFMxCzAJBgNVBAYT
AlVTMRMwEQYDVQQKEwpBbWF6b24uY29tMQwwCgYDVQQLEwNBV1MxITAfBgNVBAMT
GEFXUyBMaW1pdGVkLUFzc3VyYW5jZSBDQTAeFw0xMjEwMDUxMjQzNDdaFw0xMzEw
MDUxMjQzNDdaMFIxCzAJBgNVBAYTAlVTMRMwEQYDVQQKEwpBbWF6b24uY29tMRcw
FQYDVQQLEw5BV1MtRGV2ZWxvcGVyczEVMBMGA1UEAxMMZDhoZmxqbzVkaXIxMIGf
MA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCU1+xvbyoTFXcfhpUfTmQPpPlNcusN
2WFB9c3w9eI/s+P0yZ6bxuajFzA7Y605yTth2wi9YvkiRxiM4alA/+2Gwribii+8
fB9P0nq9V4HQjXDLt2GxJMQRVJCIaqQR2paxqv2Zvow2girWg9DO2b+MwuFuf5gr
QbcAP9R5IvnFVQIDAQABo1cwVTAOBgNVHQ8BAf8EBAMCBaAwFgYDVR0lAQH/BAww
CgYIKwYBBQUHAwIwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUxo3xUKXYAIIgBk91
aD6nOjjqAVYwDQYJKoZIhvcNAQEFBQADgYEAkGr95/SQe2RaBuB4hoixUeWnpY3w
O0zhG7LSZuKHw3JflXZ5ikW8c+JmoZRQoMvM6K1ki5DUPkFjPFLtNZX+GmBioMyM
vuo3RSTtBCQeyEIg95omvbq8zvyWKgiFsTg9+dRcNrutfaawuEqVx6tfvjCs7pS7
/7Mkd/LZT2qfozU=
-----END CERTIFICATE-----"""
}


# SERVERS LOGIC
@task
def backup_json():
    """
        Backup servers on central server
    """
    print cyan('> Servers sending to remote server')
    put(os.path.join(home_folder, 'servers.json'), remote_folder)
    print green('>\tServers saved on %s' % current()['alias'])


@task
def update_json():
    """
    Update servers from remote server
    """
    print cyan('> Servers getting from remote server')
    scp_get('servers.json', home_folder)
    print green('>\tServers got from remote server')


class ServerList(dict):
    def __init__(self):
        self.load()
        self.certs = certs
        self.by_tags = partial(self.by_attrs, 'tags')
        self.by_groups = partial(self.by_attrs, 'groups')
        self.by_projects = partial(self.by_attrs, 'projects')
        self.by_hosts = partial(self.by_attrs, 'other_hosts')
        print green('>\tServers loaded')

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
            print cyan('> Local servers.json existed')
            with file(os.path.join(home_folder, 'servers.json'), 'r') as f:
                self.update(json.loads(f.read()))
        else:
            print yellow('> No local servers.json')
            # execute(update_json, hosts=[central_server])
            # update_json()
            print cyan('> Servers getting from remote server')
            os.system('scp %s:servers.json %s' % (central_server, home_folder))
            print green('>\tServers got from remote server')
            self.load()


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
    print cyan('> Servers getting file from S3')
    b = get_bucket(bucket)
    k = b.get_key(filename)
    print green('>\tServers got %s from S3' % filename)
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
for cert in certs:
    env.key_filename.append(dump_to_file(cert, certs[cert], 400))

SERVERS = ServerList()

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


# SERVE LOGIC

try:
    from bottle import route, request, HTTPError
    from bottle import run as server_run
    from jinja2 import Template

    @route('/')
    def dump():
        if not serve_key in request.GET:
            raise HTTPError(404, "These are not the droids you're looking for")
        hosts = sum([a['other_hosts'] for a in SERVERS.values()], [])
        hosts.extend(sorted(list(set([a['host'] for a in SERVERS.values()])))[1:])
        tags = list(set(sum([a['tags'] for a in SERVERS.values()], [])))
        groups = list(set(sum([a['groups'] for a in SERVERS.values()], [])))
        ips = [a['ip'] for a in SERVERS.values()]

        return Template(get_s3_var('nervarin.html')).render(servers=SERVERS.iteritems(),
            certs=SERVERS.certs,
            tags=tags,
            hosts=hosts,
            groups=groups,
            ips=ips,
            key=serve_key
            )

    @route('/search')
    def search():
        _query = map(lambda x: x.strip(' "'), request.GET['q'].split(' '))
        query = {}
        for i, f in enumerate(_query):
            if f.endswith(':'):
                if not f.strip(':') in query:
                    query[f.strip(':')] = []
                query[f.strip(':')].append(_query[i + 1])
        res = map(lambda x: x['alias'], SERVERS.values())
        bt = bg = bh = bi = []
        if 'tag' in query:
            bt = map(lambda x: x['alias'], SERVERS.by_tags(*query['tag']))
        if 'group' in query:
            bg = map(lambda x: x['alias'], SERVERS.by_groups(*query['group']))
        if 'host' in query:
            for s in SERVERS:
                SERVERS[s]['hosts'] = SERVERS[s]['other_hosts'] + [SERVERS[s]['host']]
            bh = map(lambda x: x['alias'], SERVERS.by_attrs('hosts', *query['host']))
        if 'ip' in query:
            bi = map(lambda x: x['alias'], SERVERS.by_attr('ip', query['ip'][0]))
        for r in [bt, bg, bh, bi]:
            if r:
                res = set(res) & set(r)
        return json.dumps({'res': list(set(res))})

    @task
    def serve():
        """
            Run web-server for html version of servers list
        """
        server_run(host='0.0.0.0', port=PORT, reloader=True, server='twisted')

except:
    print red('Serve not supported. Need Bottle and Jinja2')


# FABRIC LOGIC
@task
def shell(native=False, tmux=True):
    """
        Open common ssh shell
    """
    if native or eval(str(native)):
        print cyan('> Opening native fabric shell')
        open_shell(ssh_startup if eval(str(tmux)) else '')
    else:
        print cyan('> Opening ssh shell')
        key = current()['ssh_cert']
        password = SERVERS.by_attr('ip', env['host_string'].split('@')[1].split(':')[0])[0]['ssh_password']
        if key:
            key = '-i .temp/' + key
        ssh = "sshpass -p '%s' ssh %s -p %s %s -t '%s'" % (password,
            env['host_string'].split(':')[0],
            env['host_string'].split(':')[1],
            key,
            ssh_startup if eval(str(tmux)) else '')
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
@parallel
def init(full=False):
    """
        Install must-have tools like tmux, zsh and others
    """
    env.warn_only = True
    if eval(str(full)):
        print cyan('> Perfom full init')
        for p in packages:
            install(p)
        for p in pip_packages:
            pip(p)
        run('curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh')
    env.warn_only = False
    print cyan('Renew configs')
    path = run('which zsh')
    put(dump_to_file('.tmux.conf', get_s3_var('tmux.conf').replace('{{shell}}', path)), '.')
    put(dump_to_file('.zshrc', Template(
        get_s3_var('zshrc')).render({
            'server': current()['alias'],
            'aliases': aliases,
            'color': current().get('color', None)
            })), '.')
    for cf in cloud_files:
        run('wget "https://s3.amazonaws.com/%(bucket)s/%(key)s" -O %(path)s' % cf)
    # clean()


@task
def get_info():
    """
        Get server info
    """
    print cyan('> Getting server info')
    import pprint
    # from pygments import highlight
    # from pygments.lexers import JSONLexer
    # from pygments.formatters import Terminal256Formatter
    # print green('>\t"%s" server info' % current()['alias'])
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
    print cyan('> Performing full backup')
    backup_json()
    print cyan('> Nervarin sending to remote server')
    put(env['fabfile'], remote_folder)
    print green('>\tNervarin saved on %s' % current()['alias'])


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
def test():
    print env


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


if __name__ == "__main__":
    os.system('ipython --quick -c "import nervarin as n" -i')
