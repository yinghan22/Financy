"""
@file    : EcoClassService.py
@author  : zhufengshuo/朱凤硕
@email   : 2257956934@qq.com
@create  : 2023/05/03 11:25
"""

from models import EcoClassModel
from utils.CRUD import crud
from utils.Module import Module

module_ecoclass = Module('economy', url_prefix='/api/economy')


@crud
class EcoClassService:
    Model = EcoClassModel

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def after_update(cls, data):
        return None


module_ecoclass.router_list([
    ('', EcoClassService.Select),
    ('', EcoClassService.Create),
    ('/<id:int>', EcoClassService.SelectIn),
    ('/<id:int>', EcoClassService.Update),
    ('/<id:int>', EcoClassService.Delete),
    ('/<name:str>/<value>', EcoClassService.SelectBy)
])
