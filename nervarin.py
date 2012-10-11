# -*- coding: utf-8 -*-
from functools import partial


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


servers = {
    'dev': {
        'ip': '10.137.190.6',
        'os': 'linux',
        'host': 's4.lcs.local',
        'other_hosts': [
            'dev.lcs.local',
            'gitlab.lcs.local',
            'emercom.lcs.local',
            'sentry.lcs.local'
        ],
        'tags': ['work', 'spb'],
        'projects': ['dev', 'emercom', 'api'],
        'ssh_port': 22,
        'ssh_user': 'nabrodov',
        'ssh_password': 'aqwersdf',
        'ssh_cert': '',
        'ftp_port': 21,
        'description': 'Work dev server',
    },
    'note': {
        'ip': '10.137.190.141',
        'os': 'linux',
        'host': '',
        'other_hosts': [],
        'tags': ['work', 'spb'],
        'projects': ['dev', 'emercom', 'api'],
        'ssh_port': 22,
        'ssh_user': 'nabrodov',
        'ssh_password': 'aqwersdf',
        'ssh_cert': '',
        'ftp_port': 21,
        'description': 'Work demo server'
    },

    'moscow_linux': {
        'ip': '10.137.190.77',
        'os': 'linux',
        'host': '',
        'other_hosts': [],
        'tags': ['work', 'moscow'],
        'projects': ['dev', 'emercom', 'api'],
        'ssh_port': 22,
        'ssh_user': 'root',
        'ssh_password': 'vjrhtvt17',
        'ssh_cert': '',
        'ftp_port': 21,
        'description': 'Moscow server linux (Emercom 2.0)',
        'keys': {
            'oracle_user': 'service2',
            'oracle_pass': 'gwlxTjK'
        }
    },
    'moscow_win': {
        'ip': '10.137.190.62',
        'os': 'windows',
        'host': '',
        'other_hosts': [],
        'tags': ['work', 'moscow'],
        'projects': [],
        'ftp_port': 21,
        'description': 'Moscow server windows (Emercom 2.0)',
        "keys": {
            'rdp_user': 'administartor',
            'rdp_password': 'vjrhtvt17'
        }
    },


    'clodo': {
        'ip': '62.76.40.97',
        'os': 'linux',
        'host': 'averr.in',
        'other_hosts': ['me.averr.in'],
        'tags': ['private'],
        'projects': ['eliar'],
        'ssh_port': 22,
        'ssh_user': 'averrin',
        'ssh_password': 'aqwersdf',
        'ssh_cert': '',
        'ftp_port': 21,
        'description': 'Clodo private server'
    },
    'home': {
        'ip': '109.230.153.135',
        'os': 'linux',
        'host': 'home.averr.in',
        'other_hosts': [],
        'tags': ['private'],
        'projects': [],
        'ssh_port': 8822,
        'ssh_user': 'averrin',
        'ssh_password': 'aqwersdf',
        'ssh_cert': '',
        'ftp_port': 8821,
        'description': 'Home media server (Stora)'
    },
    'aws': {
        'ip': '107.22.234.119',
        'os': 'linux',
        'host': 'aws.averr.in',
        'other_hosts': [],
        'tags': ['private', 'aws'],
        'projects': ['evernight'],
        'ssh_port': 22,
        'ssh_user': 'averrin',
        'ssh_password': '',
        'ssh_cert': 'aws_ssh_averrin',
        'ftp_port': 21,
        'description': 'Amazon cloud server',
        "keys": {
            "aws_id": 'AKIAIQ4CB4POAICCQVIA',
            "aws_key": 'SbTGinDN+P5n0IIGmvc4CwVzZFb2IojtG9Q9dF+O'
        }
    }
}


template = """
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
    <div style="width: 400px; margin: 6px auto;">
        {% for name,s in servers %}
            <div class="well">
                <h4>{% if s.host %}{{s.host}}{% else %}{{name}}{% endif %} <span class="label">{{s.os}}</span></h4>
                <strong>IP:</strong> {{s.ip}} <br />
                {% if s.os=="linux" %}<strong>SSH:</strong> ssh {{s.ssh_user}}{% if s.ssh_password %}:{{s.ssh_password}}{% endif %}@{% if s.host %}{{s.host}}{% else %}{{s.ip}}{% endif %} -p {{s.ssh_port}} <br />{% endif %}
                {% if s.os=="linux" %}<strong>FTP port:</strong> {{s.ftp_port}} <br />{% endif %}
                {% if s.other_hosts %}<strong>other_hosts:</strong> {{s.other_hosts|join(', ')}} <br />{% endif %}
                <strong>Tags:</strong> {% for tag in s.tags %}<span class="label label-success">{{tag}}</span> {% endfor %}
            </div>
        {% endfor %}
    </div>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.1.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""


from bottle import route, run


class ServerList(dict):
    def __init__(self):
        self.update(servers)
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

SERVERS = ServerList()


@route('/')
def dump():
    from jinja2 import Template
    return Template(template).render(servers=SERVERS.iteritems(), certs=SERVERS.certs)


def serve():
    run(host='0.0.0.0', port=8080, reloader=True)

if __name__ == "__main__":
    serve()
