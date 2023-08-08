from selectorlib import Extractor
import requests

YAML_STRING = """
categories:
    css: 'div.a-subheader ul.a-unordered-list'
    xpath: null
    type: Text
title:
    css: 'h1.a-size-large span.a-size-large'
    xpath: null
    type: Text
selling_price1:
    css: 'td.a-span12 span.a-price.a-size-medium span:nth-of-type(2)'
    xpath: null
    type: Text
mrp1:
    css: 'td.a-span12.a-color-secondary span.a-price span:nth-of-type(2)'
    xpath: null
    type: Text
description:
    css: 'div.a-section.a-spacing-medium span.a-list-item'
    xpath: null
    multiple: true
    type: Text
attribute_keys1:
    css: 'td.a-span3 span.a-size-base'
    xpath: null
    multiple: true
    type: Text
attribute_values1:
    css: 'td.a-span9 span.a-size-base'
    xpath: null
    multiple: true
    type: Text
rating1:
    css: 'div.centerColAlign span.reviewCountTextLinkedHistogram a.a-popover-trigger'
    xpath: null
    type: Text
mrp2:
    css: 'span.a-size-small span.a-price span:nth-of-type(2)'
    xpath: null
    type: Text
selling_price2:
    css: 'div.centerColAlign span.a-price-whole'
    xpath: null
    type: Text
attribute_keys2:
    css: 'div.a-expander-content table.a-keyvalue th.a-color-secondary'
    xpath: null
    multiple: true
    type: Text
attribute_values2:
    css: 'div.a-expander-content td.a-size-base'
    xpath: null
    multiple: true
    type: Text
rating2:
    css: 'div.a-section div.celwidget span.reviewCountTextLinkedHistogram a.a-popover-trigger'
    xpath: null
    type: Text
ranks1:
    css: 'div.a-section.feature > ul.a-unordered-list:nth-of-type(1) > li > span.a-list-item'
    xpath: null
    type: Text
ranks2:
    css: 'div.a-section div.a-section tr:nth-of-type(3) td'
    xpath: null
    type: Text
number_of_ratings:
    css: 'div.centerColAlign span.a-declarative span.a-size-base'
    xpath: null
    type: Text
store:
    css: 'div#bylineInfo_feature_div.celwidget div.a-section'
    xpath: null
    type: Text
product_details_keys1:
    css: 'div.a-section.feature div span.a-text-bold'
    xpath: null
    multiple: true
    type: Text
product_details_values1:
    css: 'div.a-section div span.a-list-item span:nth-of-type(2)'
    xpath: null
    multiple: true
    type: Text
product_details_keys2:
    css: 'div.a-section div.a-section th.a-color-secondary'
    xpath: null
    multiple: true
    type: Text
product_details_values2:
    css: 'div.a-section div.a-section td'
    xpath: null
    multiple: true
    type: Text
"""


class ProductDetailsExtractor:
    def __init__(self):
        self._amazon_product_extractor = Extractor.from_yaml_string(
            YAML_STRING)

    def __scrape(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '2',
            'ect': '4g',
            'rtt': '250',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '2',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua-platform-version': '"6.0"',
            'sec-ch-viewport-width': '400',
            'viewport-width': '400'
        }

        r = requests.get(url, headers=headers)

        if r.status_code > 500:
            raise Exception(
                "Page %s was blocked by Amazon. Please try using better proxies." % url)
        else:
            return self._amazon_product_extractor.extract(r.text)

    def __process_categories(self, data):
        categories = data['categories']
        if categories:
            return categories.split(' › ')
        return None

    def __process_mrp(self, data):
        mrp1 = data['mrp1']
        mrp2 = data['mrp2']
        mrp = next((mrp for mrp in [
            mrp1, mrp2] if mrp), None)
        return mrp

    def __process_selling_price(self, data):
        selling_price1 = data['selling_price1']
        selling_price2 = data['selling_price2']
        selling_price = next((selling_price for selling_price in [
            selling_price1, selling_price2] if selling_price), None)
        return selling_price

    def __process_ranks(self, data):
        ranks1 = data['ranks1']
        ranks2 = data['ranks2']
        ranks = next((ranks for ranks in [
            ranks1, ranks2] if ranks), None)

        processed_ranks = []

        if ranks and '#' in ranks:
            while '#' in ranks:
                rank_start = ranks.index('#')
                rank_end = ranks.index(' ', rank_start)

                category_start = rank_end + 3
                category_end = len(ranks)
                if '(' in ranks[category_start:] and '#' in ranks[category_start:]:
                    category_end = min(ranks.index(
                        '(', category_start), ranks.index('#', category_start))
                elif '#' in ranks[category_start:]:
                    category_end = ranks.index('#', category_start)

                processed_ranks.append({
                    'rank': int(ranks[rank_start + 1:rank_end].replace(',', '').strip()),
                    'category': ranks[category_start:category_end].strip()
                })

                ranks = ranks[category_end:]

        return processed_ranks or None

    def __process_rating(self, data):
        rating1 = data['rating1']
        rating2 = data['rating2']
        rating = next(
            (rating for rating in [rating1, rating2] if rating), None)

        if rating:
            rating = rating.replace('out of 5 stars', '').strip()

        return rating

    def __process_attributes(self, data):
        processed_properties = []

        for i in range(1, 3):
            attribute_keys = data['attribute_keys'+str(i)]

            if attribute_keys:
                values = data['attribute_values'+str(i)]

                if len(values) > len(attribute_keys):
                    values = values[len(values)-len(attribute_keys):]

                for j in range(len(attribute_keys)):
                    property = {
                        'name': str(attribute_keys[j]),
                        'value': str(values[j])
                    }
                    processed_properties.append(property)

        return processed_properties or None

    def __process_product_details(self, data):
        processed_properties = []

        for i in range(1, 3):
            product_details_keys = data['product_details_keys'+str(i)]

            if product_details_keys:
                values = data['product_details_values'+str(i)]
                if len(values) > len(product_details_keys):
                    values = values[len(values)-len(product_details_keys):]

                for j in range(len(product_details_keys)):
                    property = {
                        'name': str(product_details_keys[j]).replace('\n', '').replace(':', '').replace('\u200e', '').replace('\u200f', '').strip(),
                        'value': str(values[j])
                    }
                    processed_properties.append(property)

        return processed_properties or None

    def __process_store(self, data):
        store = data['store']
        if store:
            store = store.replace('Visit the', '').replace(
                'Store', '').replace('Brand:', '').strip()
        return store

    def __process_number_of_ratings(self, data):
        number_of_ratings = data['number_of_ratings']
        if number_of_ratings:
            number_of_ratings = number_of_ratings.replace(
                'ratings', '').strip()
        return number_of_ratings

    def __clean_data(self, data):
        data.pop('selling_price1', None)
        data.pop('selling_price2', None)
        data.pop('mrp1', None)
        data.pop('mrp2', None)
        data.pop('attribute_keys1', None)
        data.pop('attribute_keys2', None)
        data.pop('attribute_values1', None)
        data.pop('attribute_values2', None)
        data.pop('rating1', None)
        data.pop('rating2', None)
        data.pop('ranks1', None)
        data.pop('ranks2', None)
        data.pop('product_details_keys1', None)
        data.pop('product_details_keys2', None)
        data.pop('product_details_values1', None)
        data.pop('product_details_values2', None)

        return data

    def __process_data(self, data):
        data['categories'] = self.__process_categories(data)
        data['mrp'] = self.__process_mrp(data)
        data['selling_price'] = self.__process_selling_price(data)
        data['ranks'] = self.__process_ranks(data)
        data['rating'] = self.__process_rating(data)
        data['key_features'] = self.__process_attributes(data)
        data['product_details'] = self.__process_product_details(data)
        data['store'] = self.__process_store(data)
        data['number_of_ratings'] = self.__process_number_of_ratings(data)

        data = self.__clean_data(data)

        return data

    def get_product_from_url(self, url):
        data = self.__scrape(url)
        processed_data = self.__process_data(data)
        return processed_data

    def get_product_from_asin_code(self, asin_code):
        url = 'https://www.amazon.in/dp/'+asin_code.upper()
        data = self.__scrape(url)
        processed_data = self.__process_data(data)
        return processed_data
