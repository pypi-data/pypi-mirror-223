from datetime import datetime
from dateutil import parser

from typing import (
    Text,
    Any
)

import warnings
import contextlib

import requests
from urllib3.exceptions import InsecureRequestWarning

old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass
            
class Utils():
    
    @staticmethod
    def get_dict_val(data:dict, key:Text, default=None):
        try:
            if data is not None and key is not None:
                return data.get(key, default)
        except:
            pass
        return default
    
    @staticmethod
    def to_datetime(dtime:Text) -> datetime:
        if dtime is None or len(dtime) == 0:
            return None
        
        try:            
            return parser.parse(dtime)
        except:
            pass

        return None 