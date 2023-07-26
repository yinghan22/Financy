"""
@file    : BaseView.py
@email   : yinghan22@163.com
@author  : yinghan/嬴寒
@created : 2023/04/03 19:09
"""
import math

import pypinyin
from sanic.views import HTTPMethodView

from utils.Response import Response


def is_number(value: str):
    if type(value) is not str:
        raise ValueError('传入的参数必须是字符串！')
    if value[0].isalpha():
        return False
    if len(value) > 2 and value.count('.', 1, -1) == 1:
        value = value.replace('.', '', 1)
    if value.isnumeric():
        return True
    else:
        return False


def pinyin(value: str):
    res = pypinyin.pinyin(value, style=pypinyin.FIRST_LETTER)
    res = ''.join([item[0] for item in res]).upper()
    return res


class BaseView(HTTPMethodView):
    response = Response()

    @classmethod
    def success(
            cls,
            data: object = None,
            message: str = "success",
            status: int = 200,
            page_info: dict = None,
    ):
        return cls.response.success(data, message, status, page_info)

    @classmethod
    def error(
            cls,
            data: object = None,
            message: str = "Error",
            status: int = 400,
            page_info: dict = None,
    ):
        return cls.response.error(data, message, status, page_info)

    @classmethod
    def bad_request(
            cls, data: object = None, message: str = "Error: Bad Request", status: int = 400
    ):
        return cls.response.bad_request(data, message, status)

    @classmethod
    def sort(cls, data: list, request, default_field) -> None:
        """sort for dict
        默认 升序
        :param default_field: 
        :param data: 欲排序的列表
        :param request:
        """
        sort_by = request.args.get("sort_by", default_field)
        reverse = request.args.get('reverse', '').lower() in ['true', '1']
        if len(data) in [0, 1]:
            return
        if sort_by not in data[0]:
            raise AttributeError(
                "there is no attribute named {} in data:dict".format(sort_by)
            )

        data.sort(key=lambda e: int(e[sort_by]) if is_number(str(e[sort_by])) else e[sort_by], reverse=reverse)

    @classmethod
    def paginate(cls, data, request):
        length = len(data)

        if length in [0, 1]:
            return data, {
                'page_number': 1,
                'total': 1,
                'page_size': 1,
                'page': 1
            }

        current_page = int(request.args.get("current_page", 1))

        page_size = int(request.args.get('page_size', length))
        page_size = length if page_size < 0 else page_size

        total_page: int = math.ceil(length / page_size)

        if current_page > total_page:
            current_page = total_page
        elif current_page <= 0:
            current_page = 1

        page_info = {
            'page_number': total_page,
            'total': length,
            'page_size': page_size,
            'page': current_page
        }

        start = page_size * (current_page - 1)
        end = page_size * current_page

        result = data[start:end]

        return result, page_info

    @classmethod
    def pinyin(cls, value: str):
        res = pypinyin.pinyin(value, style=pypinyin.FIRST_LETTER)
        res = ''.join([item[0] for item in res]).upper()
        return res
