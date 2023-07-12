from models import VetGroup, Employee, Vetter
from utils.CRUD import crud
from utils.Module import Module

module_vetgroup = Module('vetgroup', url_prefix='/api/group')


@crud
class VetGroupService:
    Model = VetGroup

    @classmethod
    async def before_create(cls, request, param):
        if not param['name'] or param['name'] == '':
            raise ValueError('分组名称不得为空')
        if await VetGroup.filter(name=param['name']).exists():
            raise ValueError('分组名称已存在')
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def after_select(cls, data):
        user_temp = await Employee.all().values()
        user_list = {item['id']: item['name'] for item in user_temp}
        for item in data:
            item['member'] = await Vetter.filter(group_id=item['id']).values()
            tag = ''

            for n in item['member']:
                n['name'] = user_list[n['expert_id']]
                if tag == '':
                    tag = n['name']
                else:
                    tag += f", {n['name']}"
            item['tag'] = tag
        return data

    @classmethod
    async def before_update(cls, request, param, data):
        if 'name' in param:
            if await VetGroup.filter(name=param['name']).exists():
                raise ValueError('分组名称已存在')
        return param

    @classmethod
    async def after_update(cls, data):
        return None

    @classmethod
    async def after_delete(cls, id):
        await Vetter.filter(group_id=id).delete()


module_vetgroup.router_list([
    ('', VetGroupService.Create),
    ('', VetGroupService.Select),
    ('/<id:int>', VetGroupService.SelectIn),
    ('/<id:int>', VetGroupService.Update),
    ('/<id:int>', VetGroupService.Delete),
    ('/<name:str>/<value>', VetGroupService.SelectBy)
])
