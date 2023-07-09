from models import Vetter, Employee, VetGroup
from utils.CRUD import crud
from utils.Module import Module

module_vetter = Module('vetter', url_prefix='/api/vetter')


@crud
class VetterService:
    Model = Vetter

    @classmethod
    async def before_create(cls, request, param):
        __user__ = await Employee.filter(id=param['user_id']).exists()
        if not __user__:
            raise ValueError('目标用户不存在')
        __group__ = await VetGroup.filter(id=param['group_id']).exists()
        if not __group__:
            raise ValueError('目标分组不存在')
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def after_update(cls, data):
        return None


module_vetter.router_list([
    ('/', VetterService.Create),
    ('/', VetterService.Select),
    ('/<id:int>', VetterService.Update),
    ('/<id:int>', VetterService.Delete),
    ('/<name:str>/<value>', VetterService.SelectBy)
])
