"""
@file    : Module.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/04/09 14:44
"""
from sanic import Blueprint


class Module(Blueprint):
    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)

    def router(self, handler, url):
        self.add_route(handler.as_view(), url)

    def router_list(self, handler_url_list, prefix=''):
        prefix = prefix.strip()
        if not prefix.startswith('/') and prefix != '':
            prefix = '/{}'.format(prefix)
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        for url, handler in handler_url_list:
            url = url.strip()
            if not url.startswith('/') and prefix != '':
                url = '/{}'.format(url)
            if url != '/' and url.endswith('/'):
                url = url[:-1]

            self.add_route(handler.as_view(), '{}{}'.format(prefix, url))
