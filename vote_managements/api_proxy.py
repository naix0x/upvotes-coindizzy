import requests
from multiprocessing import Pool
from vote_managements.proxy import get_proxies_from_url, test_proxy
from vote_managements.target import URL_COINDIZZY_VOTE, URL_COINDIZZY_WATCHLIST, HEADERS_COINDIZZY

def main():
    proxy_urls = [
        "https://openproxylist.xyz/http.txt",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    ]

    all_urls = [URL_COINDIZZY_VOTE, URL_COINDIZZY_WATCHLIST]
    all_proxies = []

    for url in proxy_urls:
        all_proxies.extend(get_proxies_from_url(url))

    with Pool(processes=8) as pool:
        for url in all_urls:
            pool.starmap(test_proxy, [(proxy, url, HEADERS_COINDIZZY) for proxy in all_proxies])

if __name__ == "__main__":
    main()
