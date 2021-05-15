import re

import requests
import grequests
# from fake_useragent import UserAgent

from sbml2json.db import get_connection
from sbml2json.util.proxy import get_random_requests_proxies
from sbml2json.util._dict import merge_dict

# user_agent = UserAgent(verify_ssl = False)

# https://git.io/JsnSI
_REGEX_URL = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def proxy_request(*args, **kwargs):
    fallback = kwargs.pop("fallback", False)

    session  = requests.Session()

    proxies = get_random_requests_proxies()
    # session.headers.update({ "User-Agent": user_agent.random })
    session.proxies.update(proxies)

    try:
        response = session.request(*args, **kwargs, timeout = 5)
    except requests.exceptions.ConnectionError as e:
        if fallback:
            session.headers = kwargs.get("headers", {})
            session.proxies = kwargs.get("proxies", {})
            response = session.request(*args, **kwargs)
        else:
            raise e

    return response

def proxy_grequest(*args, **kwargs):
    proxies = get_random_requests_proxies()
    
    # kwargs["headers"] = merge_dict(kwargs.get("headers", {}), {
    #     "User-Agent": user_agent.random })
    kwargs["proxies"] = merge_dict(kwargs.get("proxies", {}), proxies)

    return grequests.request(*args, **kwargs)

def check_url(url, raise_err = True):
    if not re.match(_REGEX_URL, url):
        if raise_err:
            raise ValueError("Invalid URL: %s" % url)
        
        return False
    
    return True