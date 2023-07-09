from models import VetGroup, Employee
from utils.CRUD import crud
from utils.Module import Module

module_vetgroup = Module('vetgroup', url_prefix='/api/vetgroup')


@crud
class VetGroupService:
    Model = VetGroup

    @classmethod
    async def before_create(cls, request, param):
        if not param['name'] or param['name'] == '':
            raise ValueError('分组名称不得为空')
        if await VetGroup.filter(param['name']).exists():
            raise ValueError('分组名称已存在')
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def after_select(cls, data):
        for item in data:
            group_user = await Employee.filter(group_id=item['id']).values()
            label = ''
            for user in group_user:
                if label == '':
                    label = user['name']
                else:
                    label += f", {user['name']}"
            item['label'] = label
        return data

    @classmethod
    async def before_update(cls, request, param, data):
        if 'name' in param:
            if await VetGroup.filter(param['name']).exists():
                raise ValueError('分组名称已存在')
        return param

    @classmethod
    async def after_update(cls, data):
        return None


module_vetgroup.router_list([
    ('', VetGroupService.Create),
    ('', VetGroupService.Select),
    ('/<id:int>', VetGroupService.Update),
    ('/<id:int>', VetGroupService.Delete),
    ('/<name:str>/<value>', VetGroupService.SelectBy)
])
