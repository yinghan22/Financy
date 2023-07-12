"""
@file    : DepartmentService.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/4/29 下午5:09
"""

from models import Department
from utils.BaseView import pinyin
from utils.CRUD import crud
from utils.Module import Module

module_department = Module('dept', url_prefix='/api/dept')


@crud
class DeptService:
    Model = Department

    @classmethod
    async def before_create(cls, request, param):
        if not param['name'] or param['name'] == '':
            raise ValueError('请输入部门名称')
        __data__ = await cls.Model.filter(name=param['name']).exists()
        if __data__:
            raise ValueError('部门名称已存在')
        param['pinyin'] = pinyin(param['name'])
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def before_update(cls, request, param, data):
        if not param['name'] or param['name'] == '':
            raise ValueError('部门名称不得为空')
        param['pinyin'] = pinyin(param['name'])
        return param

    @classmethod
    async def after_update(cls, data):
        return None


module_department.router_list([
    ('', DeptService.Select),
    ('', DeptService.Create),
    ('/<id:int>', DeptService.SelectIn),
    ('/<id:int>', DeptService.Update),
    ('/<id:int>', DeptService.Delete),
    ('/<name:str>/<value>', DeptService.SelectBy)
])
