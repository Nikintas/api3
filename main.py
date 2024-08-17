from dotenv import load_dotenv
from urllib.parse import urlparse
from requests.exceptions import HTTPError
import os
import requests
import argparse


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {"Authorization": f"Bearer {token}"}
    params = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {"Authorization": f"Bearer {token}"}
    params = {'unit': 'day', 'units': '-1'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bitlink):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Эта программа сокрощяет ссылки и получать клики по уже сокращёным ссылкам')
    parser.add_argument('--url', help='Введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f'{parsed_url.netloc}{parsed_url.path}'
    try:
        if is_bitlink(token, parsed_url):
            print('Количество кликов', count_clicks(token, parsed_url))
        else:
            print('Битлинк', shorten_link(token, args.url))
    except HTTPError as error:
        print('Проверьте ссылку на корректность', error)
