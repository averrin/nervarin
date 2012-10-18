#!/usr/bin/env python
# -*- coding: utf-8 -*-

#MODULES

try:
    from functools import partial
    from fabric.api import run, env, open_shell, put, sudo, get, prompt, puts
    from fabric.colors import red
    from fabric.decorators import task
    from fabric.tasks import execute
    import os
    import shutil
    import json
except ImportError:
    print 'Plz install deps:'
    print '>\tsudo pip install fabric bottle boto'
    exit(1)


# CONFIG
PORT = 8080
serve_key = 'aqwersdf'
ssh_startup = 'tmux new-session -t default || tmux new-session -s default'
packages = ['tmux', 'zsh', 'curl', 'w3m', 'autojump', 'vim']
pm_args = {'apt-get': '-ym --force-yes', 'yum': '-y'}

central_server = 'averrin@aws.averr.in:22'
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

TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Nervarin</title>
    <!-- Bootstrap -->
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/css/bootstrap-combined.min.css" rel="stylesheet">
    <!-- <link rel="stylesheet" href="http://averr.in/static/gen/bp_packed.css?1311598113">
    <link rel="stylesheet" href="http://averr.in/static/gen/packed.css?1304342019"> -->
  </head>
  <body>
    <div class="row-fluid" style="padding-top: 6px;">
        {% for name,s in servers %}
            <div class="well span4" style="height: 300px; margin-left: 6px; overflow-y: auto;">
                <h4>{{s.alias}} <small>{% if s.host %}{{s.host}}{% else %}{{s.ip}}{% endif %}</small></h4>
                <strong>IP:</strong> {{s.ip}} <br />
                <strong>OS:</strong> {{s.os}} <br />
                {% if s.os=="linux" %}<strong>SSH:</strong> ssh {{s.ssh_user}}{% if s.ssh_password %}:{{s.ssh_password}}{% endif %}@{% if s.host %}{{s.host}}{% else %}{{s.ip}}{% endif %} -p {{s.ssh_port}} <br />{% endif %}
                {% if s.os=="linux" %}<strong>FTP port:</strong> {{s.ftp_port}} <br />{% endif %}
                {% if s.other_hosts %}<strong>other_hosts:</strong> {{s.other_hosts|join(', ')}} <br />{% endif %}
                <strong>Tags:</strong> {% for tag in s.tags %}<span class="label label-success">{{tag}}</span> {% endfor %} <br />
                {% if s.attrs %}
                    <strong>Attributes:</strong>
                    <ul>
                        {% for k,v in s.attrs.iteritems() %}
                        <li><strong>{{k}}:</strong> {{v}}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
                {% if s.groups %}
                    <strong>Groups:</strong>
                        {% for g in s.groups %}
                            <span class="label label-info">{{g}}</span>
                        {% endfor %}
                    </ul>
                {% endif %}
            </div>
        {% endfor %}
    </div>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""

tmux_conf = """
set-option -g default-shell "{{shell}}"
unbind C-b
unbind l
set -g prefix C-a
bind-key C-a last-window
set-option -g mouse-select-pane on
unbind %
bind | split-window -h
bind - split-window -v
bind % killp
bind a displayp \; lsp
bind h neww htop
bind r source-file ~/.tmux.conf
set -g default-terminal "screen-256color"
set -g history-limit 1000
set-window-option -g mode-keys vi # vi key
set-option -g status-keys vi
set-window-option -g utf8 on
set-window-option -g mode-mouse off
set-option -g base-index 1
set-option -g status-utf8 on
set-option -g status-justify right
set-option -g status-bg black
set-option -g status-fg white
set-option -g status-interval 5
set-option -g status-left-length 30
set-option -g status-left '#[fg=red,bold]» #[fg=blue,bold]#T#[default]'
set-option -g status-right '#[fg=white,bold]»» #[fg=blue,bold]###S #[fg=red]%R %d.%m#(acpi | cut -d ',' -f 2)#[default]'
set-option -g visual-activity on
set-window-option -g monitor-activity on
set-window-option -g window-status-current-fg white
set-window-option -g window-status-current-bg default
set-window-option -g window-status-current-attr bold
set-window-option -g clock-mode-colour cyan
set-window-option -g clock-mode-style 24
set-window-option -g window-status-fg white
set-window-option -g window-status-attr dim
set -g default-terminal screen-256color
"""

zshrc = """
ZSH=$HOME/.oh-my-zsh
ZSH_THEME="sorin"
plugins=(git)
source $ZSH/oh-my-zsh.sh
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
#source /usr/share/autojump/autojump.sh
PS1="(%{$fg[cyan]%}{{server}}%{$reset_color%}) $PS1"
"""

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
    put('servers.json', '.')


@task
def update_json():
    """
    Update servers from central server
    """
    get('servers.json', '.')


class ServerList(dict):
    def __init__(self):
        self.load()
        self.certs = certs
        self.by_tags = partial(self.by_attrs, 'tags')
        self.by_projects = partial(self.by_attrs, 'projects')
        self.by_hosts = partial(self.by_attrs, 'other_hosts')

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

    def dump(self):
        with file('servers.json', 'w') as f:
            f.write(json.dumps(self, indent=4))

    def load(self):
        if os.path.isfile('servers.json'):
            with file('servers.json', 'r') as f:
                self.update(json.loads(f.read()))
        else:
            execute(update_json, hosts=[central_server])
            self.load()


# ETC
def dump_to_file(filename, text, mod=777):
    with file('.temp/' + filename, 'w') as f:
        f.write(text)
        os.system('chmod %s %s' % (mod, '.temp/' + filename))
    return '.temp/' + filename


@task
def clean():
    """
        Clean temp files
    """
    os.system('chmod 777 -R .temp')
    if os.path.isdir('.temp'):
        shutil.rmtree('.temp')


def current():
    return SERVERS.by_attr('ip', env['host_string'].split('@')[1].split(':')[0])[0]


env.key_filename = []
clean()
os.mkdir('.temp')
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
        return Template(TEMPLATE).render(servers=SERVERS.iteritems(), certs=SERVERS.certs)

    @task
    def serve():
        """
            Run web-server for html version of servers list
        """
        server_run(host='0.0.0.0', port=PORT, reloader=True)

except:
    print red('Serve not supported. Need Bottle and Jinja2')


# FABRIC LOGIC
@task
def shell(native=False, tmux=True):
    """
        Open common ssh shell
    """
    if native or eval(str(native)):
        open_shell(ssh_startup if eval(str(tmux)) else '')
    else:
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
    get(remote, local)
    # clean()


@task
def init(pm='apt-get'):
    """
        Install must-have tools like tmux, zsh and others
    """
    env.warn_only = True
    s = current()
    if not 'pm' in s:
        s['pm'] = pm
    for p in packages:
        sudo('%s install %s %s' % (s['pm'], p, pm_args[s['pm']]))
    run('curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh')
    env.warn_only = False
    path = run('which zsh')
    put(dump_to_file('.tmux.conf', tmux_conf.replace('{{shell}}', path)), '.')
    put(dump_to_file('.zshrc', zshrc.replace('{{server}}', current()['alias'])), '.')
    # clean()


@task
def get_info():
    """
        Get server info
    """
    from pprint import pprint
    pprint(current())
    run('lsb_release -a', shell=False)
    run('uname -a', shell=False)
    # clean()


@task
def full_backup():
    """
        Backup servers and this file on central server
    """
    backup_json()
    put(env['fabfile'], '.')


@task
def test():
    print env

if __name__ == "__main__":
    os.system('ipython --quick -c "import nervarin as n" -i')
