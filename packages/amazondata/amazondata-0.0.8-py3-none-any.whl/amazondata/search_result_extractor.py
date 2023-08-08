from amazondata import user_agents
from selectorlib import Extractor
import requests
import random

YAML_STRING = """
products:
    css: 'div[data-component-type="s-search-result"]'
    xpath: null
    multiple: true
    type: Text
    children:
        title:
            css: 'h2 a.a-link-normal.a-text-normal'
            xpath: null
            type: Text
        url:
            css: 'h2 a.a-link-normal.a-text-normal'
            xpath: null
            type: Link
        rating:
            css: 'div.a-row.a-size-small span:nth-of-type(1)'
            xpath: null
            type: Attribute
            attribute: aria-label
        number_of_ratings:
            css: 'div.a-row.a-size-small span:nth-of-type(2)'
            xpath: null
            type: Attribute
            attribute: aria-label
        price:
            css: 'span.a-price:nth-of-type(1) span.a-offscreen'
            xpath: null
            type: Text
        is_sponsored:
            css: span.s-label-popover-default
            xpath: null
            type: Text
"""


class SearchResultExtractor:
    def __init__(self):
        self._amazon_product_extractor = Extractor.from_yaml_string(
            YAML_STRING)

    def __scrape(self, url):
        headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': random.choice(user_agents.USER_AGENTS),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'www.amazon.in',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        r = requests.get(url, headers=headers)

        if r.status_code > 500:
            raise Exception(
                "Page %s was blocked by Amazon. Please try using better proxies." % url)
        else:
            return self._amazon_product_extractor.extract(r.text)

    def __process_rating(self, data):
        if 'rating' in data:
            rating = data['rating']

            if rating:
                rating = rating.replace('out of 5 stars', '').strip()

            return rating
        return None

    def __process_number_of_ratings(self, data):
        if 'number_of_ratings' in data:
            number_of_ratings = data['number_of_ratings']

            if number_of_ratings:
                number_of_ratings = int(
                    number_of_ratings.replace(',', '').strip())

            return number_of_ratings
        return None

    def __process_is_sponsored(self, data):
        if 'is_sponsored' in data:
            is_sponsored = data['is_sponsored']
            if is_sponsored == 'Sponsored':
                return True

        return False

    def __process_url(self, data):
        if 'url' in data:
            url = data['url']

            if url:
                url = 'https://www.amazon.in'+url

            return url
        return None

    def __process_data(self, data):
        for product in data['products']:
            product['rating'] = self.__process_rating(product)
            product['number_of_ratings'] = self.__process_number_of_ratings(
                product)
            product['is_sponsored'] = self.__process_is_sponsored(product)
            product['url'] = self.__process_url(product)

        return data

    def search(self, query, page=1):
        url = 'https://www.amazon.in/s?k='+query+'&page='+str(page)
        data = self.__scrape(url)
        processed_data = self.__process_data(data)
        return processed_data
