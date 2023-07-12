"""
@file    : ORM.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/04/09 14:45
"""
import datetime
import uuid
from typing import Optional, Union

from tortoise import fields


class DatetimeField(fields.DatetimeField):
    """重载日期时间模型字段"""

    def __init__(self, *args, **kwargs):
        super(DatetimeField, self).__init__(*args, **kwargs)

    def to_python_value(self, value) -> [str, None]:
        if value is None:
            value = None
        else:
            try:
                if type(value) == datetime:
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif type(value) is str:
                    value = value.split('.')[0]
                self.validate(value)
            except Exception as ex:
                value = super(DatetimeField, self).to_python_value(value)
        return value


class DateField(fields.DateField):
    """重载日期模型字段"""

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def to_python_value(self, value) -> [str, None]:
        if value is None:
            value = None
        else:
            try:
                if type(value) == datetime:
                    value = value.strftime("%Y-%m")
                elif type(value) == str:
                    year, month, day = map(int, value.split('-'))
                    value = datetime.date(year, month, day).strftime("%Y-%m")
                self.validate(value)
            except Exception as ex:
                value = super(DateField, self).to_python_value(value)
        return value


class UUIDField(fields.UUIDField):
    """重载UUID字段"""

    def __init__(self, **kwargs):
        super(UUIDField, self).__init__(**kwargs)

    def to_python_value(self, value) -> [str, None]:
        if value is None:
            value = None
        else:
            try:
                if type(value) == uuid:
                    value = str(value)
                self.validate(value)
            except Exception as ex:
                value = super(UUIDField, self).to_python_value(value)
        return value


fields.DatetimeField = DatetimeField
fields.DateField = DateField
fields.UUIDField = UUIDField
