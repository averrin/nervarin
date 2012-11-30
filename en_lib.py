#!/usr/bin/env python
# -*- coding: utf-8 -*-c
import urllib2
import json
from pystache import render


# SERVER = 'http://averrin.meteor.com'
SERVER = 'http://averr.in:3002'
API_ROOT = 'collectionapi'
API = '%s/%s/' % (SERVER, API_ROOT)
TOKEN = '3d714fb7-a389-4748-a781-2f9329fbc280'


def make_request(collection):
    url = API + collection
    print url
    req = urllib2.Request(url)
    req.add_header('X-Auth-Token', TOKEN)
    return urllib2.urlopen(req)

get_projects = lambda: json.load(make_request('PROJECTS'))
get_servers = lambda: json.load(make_request('SERVERS'))
get_keys = lambda: json.load(make_request('KEYS'))
get_users = lambda: json.load(make_request('PROFILES'))
get_configs = lambda: json.load(make_request('CONFIGS'))


def get_profile(username):
    users = get_users()
    # print users
    for user in users:
        if user['username'] == username:
            return user['profile']


def render_config(config, server):
    for c in get_configs():
        if c['title'] == config:
            config = c
            break
    for s in get_servers():
        if s['alias'] == server:
            servers = s
            break
    return render(config['content'], server)



if __name__ == "__main__":
    print render_config("~/.zshrc", "aws")
