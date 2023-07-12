"""
@file    : Response.py
@email   : yinghan22@163.com
@author  : yinghan/嬴寒
@created : 2023/04/04 00:27
"""
from sanic.response import JSONResponse


class Response(JSONResponse):
    __result__ = {
        'data': None,
        'status': 200,
        'message': 'success',
        'page_info': None,
    }

    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)
        # self.headers['Content-Type'] = 'application/json'

    def set(self, data: object = None, message: str = 'success', status: int = 200, page_info: dict = None):
        self.__set_data__(data)
        self.__set_message__(message)
        self.__set_status__(status)
        self.__set_page_info__(page_info)
        return self

    def success(self, data: object = None, message: str = 'success', status: int = 200, page_info: dict = None):
        self.__set_data__(data)
        self.__set_message__(message)
        self.__set_status__(status)
        self.__set_page_info__(page_info)
        return self

    def error(self, data: object = None, message: str = 'error', status: int = 400, page_info: dict = None):
        self.__set_data__(data)
        self.__set_message__(message)
        self.__set_status__(status)
        self.__set_page_info__(page_info)
        return self

    def bad_request(self, data: object = None, message: str = 'Error: Bad Request', status: int = 400):
        if message.strip() == '':
            message = 'Error: Bad Request'

        if 'page_info' in self.__result__:
            self.__result__.pop('page_info')

        self.__set_data__(data)
        self.__set_message__(message)
        self.__set_status__(status)

        return self

    def __set_data__(self, data: object = None):
        self.__result__['data'] = data
        self.set_body(self.__result__)

    def __set_message__(self, message: str = 'success'):
        if message.strip() == '':
            message = 'success'
        self.__result__['message'] = message
        self.set_body(self.__result__)

    def __set_status__(self, status: int = 200):
        if status is None:
            status = 200
        self.__result__['status'] = status
        self.set_body(self.__result__)

    def __set_page_info__(self, page_info: dict = None):
        if page_info == {}:
            page_info = None
        self.__result__['page_info'] = page_info
        if page_info is None:
            del self.__result__['page_info']
        self.set_body(self.__result__)
