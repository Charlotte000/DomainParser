import json
from threading import Thread
from types import NoneType
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def get_data(url: str, limit: int = 9999, page_num: int = 1, filtration: dict = {}, sorting: str = None) -> list[dict]:
    ''' Main function '''
    domains: list[str] = get_urls(url)

    data: list[dict] = []

    # Multithreaded data query
    threads: list[Thread] = []
    for domain in domains:
        thread = Thread(target=get_domain_data, args=(domain, data, page_num * limit))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    # Filtering
    if filtration:
        data = list(filter(_filter(filtration), data))

    # Sorting
    if sorting:
        data = sorted(data, key=_sorting(sorting))

    # Paging
    data = data[(page_num - 1) * limit : page_num * limit]

    return data


def get_urls(url: str) -> list[str]:
    ''' Parses all <a> tags on the page '''
    response = requests.get(url).content
    bs = BeautifulSoup(response, 'html.parser')
    
    result = []
    for a in bs.select('a[href^="https"]'):
        result.append(a['href'])

    return result


def get_domain_data(url: str, result: list[dict], max_length: int) -> list[dict]:
    ''' Gets domainsdb.info information '''
    domain: str = urlparse(url).netloc.removeprefix('www.')
    response = requests.get(f'https://api.domainsdb.info/v1/domains/search?domain={domain}').content
    data: dict = json.loads(response)

    if len(result) >= max_length:
        return []

    if 'domains' not in data:
        return []

    # Adding root url to the dictionary  
    for d in data['domains']:
        d['url'] = url

    result.extend(data['domains'])


def _filter(filtration: dict):
    def _wrapper(data: dict) -> bool:
        for key in filtration:
            if type(filtration[key]) in (str, NoneType, dict):
                if data[key] != filtration[key]:
                    return False
            
            if (type(filtration[key]) is list):
                if data[key] not in filtration[key]:
                    return False
                        
        return True

    return _wrapper


def _sorting(key: str):
    def _wrapper(data: dict):
        return str(data[key])
    
    return _wrapper
