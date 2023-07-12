"""
@file    : ResearchActivityService.py.py
@author  : zhufengshuo/朱凤硕
@email   : 2257956934@qq.com
@create  : 2023/04/30 20:41
"""

from models import ResearchInfo, Department
from utils.CRUD import crud
from utils.Module import Module

module_department = Module('research', url_prefix='/api/research')


@crud
class ResearchInfoService:
    Model = ResearchInfo

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教学院部名称')
        __data__ = await Department.filter(id=param['dept_id']).exists()
        if not __data__:
            raise ValueError('请输入有效的教学院部名称')
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def before_update(cls, request, param, data):
        if 'dept_id' in param:
            __data__ = await Department.filter(id=param['dept_id']).exists()
            if not __data__:
                raise ValueError('请输入有效的教学院部名称')
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


module_department.router_list([
    ('', ResearchInfoService.Select),
    ('', ResearchInfoService.Create),
    ('/<id:int>', ResearchInfoService.SelectIn),
    ('/<id:int>', ResearchInfoService.Update),
    ('/<id:int>', ResearchInfoService.Delete),
    ('/<name:str>/<value>', ResearchInfoService.SelectBy)
])
