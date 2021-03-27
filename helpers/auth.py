import json
import os

import requests


def get_auth():
    main = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(main, 'auth.json'), 'r') as f:
        auth = json.load(f)['auth']
    session_cookie = auth['cookies']['session']
    session_sig_cookie = auth['cookies']['session.sig']
    user_agent = auth['user_agent']
    formatted_cookies = f'session={session_cookie}; session.sig={session_sig_cookie}'
    return formatted_cookies, user_agent


def make_session(cookies, user_agent):
    s = requests.Session()
    s.headers.update(
        {
            'content-type': 'application/json',
            'cookie': cookies,
            'user-agent': user_agent
        }
    )
    return s
