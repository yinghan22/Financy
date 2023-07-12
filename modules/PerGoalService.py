from models import PerGoal, Department, Employee, VetGroup, Vetter
from modules.FileSercice import FileService, saveFile
from utils.CRUD import crud
from utils.Module import Module
from utils.Vetting import vetting

module_pergoal = Module('pergoal', url_prefix='/api/goal')


@crud
@vetting
class PerGoalService:
    Model = PerGoal

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')

        dept_per_goal = await cls.Model.filter(dept_id=param['dept_id']).values()
        dept_per_goal_index = 0
        if len(dept_per_goal):
            dept_per_goal_index = max([item['index'] for item in dept_per_goal])
        param['index'] = dept_per_goal_index + 1
        dept = await Department.filter(id=param['dept_id']).first().values()
        param['code'] = f"PE{dept['pinyin']}{param['index']:02d}"
        return param

    @classmethod
    async def after_create(cls, data):
        return data

    @classmethod
    async def created(cls, request, data):
        per_goal_id = data['id']
        file_list = request.files.getlist('file_list')
        if file_list:
            await saveFile(per_goal_id, file_list)
        return None

    @classmethod
    async def after_select(cls, data):
        user_temp = await Employee.all().values()
        user_list = {}
        for item in user_temp:
            user_list[item['id']] = item['name']

        group_temp = await VetGroup.all().values()
        group_list = {}
        for item in group_temp:
            __member__ = await Vetter.filter(group_id=item['id']).values()
            tag = ""
            for n in __member__:
                if tag == '':
                    tag = user_list[n['expert_id']]
                else:
                    tag += f", {user_list[n['expert_id']]}"
            group_list[item['id']] = tag
        dept_temp = await Department.all().values()
        dept_list = {}
        for item in dept_temp:
            dept_list[item['id']] = item['name']

        for item in data:
            item['file_list'] = await FileService.GetFileByPerGoalID(per_goal_id=item['id'])
            item['dept_name'] = dept_list[item['dept_id']]

            item['requester'] = str(item['requester'])
            item['requester_name'] = user_list[item['requester']]

            item['applicant_tag'] = group_list[item['applicant_id']] if item['applicant_id'] else None

        return data

    @classmethod
    async def before_update(cls, request, param, data):
        return param

    @classmethod
    async def after_update(cls, data):
        return data

    @classmethod
    async def updated(cls, request, data):
        per_goal_id = data['id']
        file_list = request.files.getlist('file_list')
        if file_list:
            await saveFile(per_goal_id, file_list)
        return None

    @classmethod
    async def after_delete(cls, request, id):
        await FileService.deleteFile(per_goal_id=id)


module_pergoal.router_list([
    ('', PerGoalService.Create),
    ('', PerGoalService.Select),
    ('/<id:int>', PerGoalService.SelectIn),
    ('/approve/<id:int>', PerGoalService.Vetting),
    ('/<id:int>', PerGoalService.Update),
    ('/<id:int>', PerGoalService.Delete),
    ('/<name:str>/<value>', PerGoalService.SelectBy)
])
