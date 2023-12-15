import random
import base64
from multiprocessing import Pool
import socks
import requests
from vote_managements.target import HEADERS_COINDIZZY

def get_proxies_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        proxies = response.text.splitlines()
        return proxies
    except Exception as e:
        print(f"Error fetching proxies from {url}: {e}")
        return []

def get_user_agents_from_file():
    with open('user-agents.txt', 'r') as file:
        user_agents = file.read().splitlines()
    return user_agents

def get_random_user_agent(user_agents):
    return random.choice(user_agents)

def test_proxy(proxy, url, headers):
    user_agents = get_user_agents_from_file()
    headers['User-Agent'] = get_random_user_agent(user_agents)

    if "@" in proxy:
        credentials, proxy = proxy.split('@')
        proxy_parts = proxy.split(':')
        protocol = proxy_parts[0].lower()

        if protocol == 'socks':
            socks_proxy = socks.ProxyType.SOCKS5 if len(proxy_parts) == 1 else socks.ProxyType.SOCKS4
            proxies = {
                'http': 'socks://{}'.format(proxy),
                'https': 'socks://{}'.format(proxy),
            }
            socks.set_default_proxy(socks_proxy, proxy_parts[1], int(proxy_parts[2]))
        else:
            proxies = {
                'http': '{}://{}'.format(protocol, proxy),
                'https': '{}://{}'.format(protocol, proxy),
            }
            headers.pop('Proxy-Authorization', None)

            if len(proxy_parts) > 1:
                proxies[protocol] = '{}://{}'.format(protocol, proxy)

            if len(proxy_parts) == 3:
                proxies[protocol] = '{}://{}'.format(protocol, proxy_parts[2])

            if len(proxy_parts) == 4:
                proxies[protocol] = '{}://{}:{}'.format(protocol, proxy_parts[2], proxy_parts[3])

            if len(proxy_parts) == 5:
                headers['Proxy-Authorization'] = 'Basic ' + base64.b64encode(proxy_parts[4].encode()).decode()
    else:
        proxies = {
            'http': 'http://{}'.format(proxy),
            'https': 'http://{}'.format(proxy),
        }
        headers.pop('Proxy-Authorization', None)

    try:
        response = requests.post(url, headers=headers, proxies=proxies, timeout=5)
        if response.ok:
            print('\033[92mProxy: {}, Response: {}, {}\033[0m'.format(proxy, response.status_code, response.text))
        else:
            print('\033[91mProxy: {}, Status: Failed, HTTP Status Code: {}\033[0m'.format(proxy, response.status_code))
    except Exception as e:
        print('\033[91mProxy: {}, Status: Failed, Error: {}\033[0m'.format(proxy, e))
