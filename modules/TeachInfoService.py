"""
@file    : TeachActivityService.py
@author  : wangxiping/王淅平
@email   : 3146453993@qqcom.com
@create  : 2023/04/30 19:16
"""

from models import TeachInfo, Department
from utils.CRUD import crud
from utils.Module import Module

module_teach = Module('teach', url_prefix='/api/teach')


@crud
class TeachInfoService:
    Model = TeachInfo

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教学院部名称')
        __data__ = await Department.filter(id=param['dept_id']).exists()
        if __data__:
            return ValueError('请输入有效的教学院部名称')

        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def before_update(cls, request, param, data):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教学院部名称')
        __data__ = await Department.filter(id=param['dept_id']).exists()
        if __data__:
            return ValueError('请输入有效的教学院部名称')
        return param

    @classmethod
    async def after_update(cls, data):
        return None

    @classmethod
    async def after_select(cls, data):
        dept_temp = await Department.all().values()
        dept_list = {item['id']: item['name'] for item in dept_temp}
        for item in data:
            item['dept_name'] = dept_list[item['dept_id']]
        return data


module_teach.router_list([
    ('/', TeachInfoService.Select),
    ('/', TeachInfoService.Create),
    ('/<id:int>', TeachInfoService.Update),
    ('/<id:int>', TeachInfoService.Delete),
    ('/<name:str>/<value>', TeachInfoService.SelectBy)
])
