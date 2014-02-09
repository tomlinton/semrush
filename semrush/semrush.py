#!/usr/bin/env python

import requests


engine_database = {
    'google.com': 'us',
    'google.us': 'us',
    'google.co.uk': 'uk',
    'google.ca': 'ca',
    'google.ru': 'ru',
    'google.de': 'de',
    'google.fr': 'fr',
    'google.es': 'es',
    'google.it': 'it',
    'google.br': 'br',
    'google.com.au': 'au',
    'google.be': 'be',
    'google.com.ar': 'ar',
    'google.mx': 'mx',
    'google.ch': 'ch',
    'google.dk': 'dk',
    'google.fi': 'fi',
    'google.ie': 'ie',
    'google.il': 'il',
    'google.nl': 'nl',
    'google.no': 'no',
    'google.pl': 'pl',
    'google.se': 'se',
    'google.com.tr': 'tr',
    'google.com.sg': 'sg',
    'google.com.hk': 'hk',
    'bing.com': 'us.bing'
}


class SemrushClientException(BaseException):

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class SemrushClient(object):

    def __init__(self, key, database='us'):
        if not key:
            raise SemrushClientException('Valid SEMRush API key required')

        if database not in engine_database.values():
            raise NotImplementedError

        self.url = 'http://%s.api.semrush.com/' % database
        self.key = key

    def get_database_from_search_engine(self, search_engine='google.com'):
        if search_engine in engine_database:
            return engine_database[search_engine]
        else:
            raise NotImplementedError

    def get_main_report(self):
        return self._call_report('domain_rank')

    def get_keyword_report(self, phrase):
        return self._call_report('phrase_this', phrase=phrase)

    def get_organic_keywords_report(self):
        return self._call_report('domain_organic')

    def get_adwords_keyword_report(self):
        return self._call_report('domain_adwords')

    def get_organic_url_report(self, url):
        return self._call_report('url_organic', url=url)

    def get_adwords_url_report(self, url):
        return self._call_report('url_adwords', url=url)

    def get_competitors_in_organic_search_report(self):
        return self._call_report('domain_organic_organic')

    def get_competitors_in_adwords_search_report(self):
        return self._call_report('domain_adwords_adwords')

    def get_potential_ad_traffic_buyers_report(self):
        return self._call_report('domain_organic_adwords')

    def get_potential_ad_traffic_sellers_report(self):
        return self._call_report('domain_adwords_organic')

    def _call_report(self, report, **kwargs):
        data = self._query(report, **kwargs)
        return self._build_report(data)

    def _build_report(self, data):
        results = []

        lines = data.split('\r')
        columns = lines[0].split(';')

        for line in lines[1:]:
            result = {}
            for i, datum in enumerate(line.split(';')):
                result[columns[i]] = datum.strip('"\n\r\t')
            results.append(result)

        return results

    def _query(self, report, **kwargs):

        universal = {
            'action': 'report',
            'type': report,
            'key': self.key,
            'export': 'api',
            'export_escape': 1
        }
        params = universal.items() + kwargs.items()
        response = requests.get(self.url, params=params)

        if response.status_code == 200:
            return response.content
        else:
            raise SemrushClientException(response.content)
