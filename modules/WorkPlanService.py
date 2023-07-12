from models import WorkPlan, Department, Employee, VetGroup, JobResp, PerGoal, Vetter
from utils.CRUD import crud
from utils.Module import Module
from utils.Vetting import vetting

module_workplan = Module('workplan', url_prefix='/api/awp')


@crud
@vetting
class WorkPlanService:
    Model = WorkPlan

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')
        if 'carry_out' in param:
            param['carry_out'] = param['carry_out'] in ['true', 'True', '1', '1']
        dept_job_resp = await cls.Model.filter(dept_id=param['dept_id']).values()
        dept_job_resp_index = 0
        if len(dept_job_resp):
            max([item['index'] for item in dept_job_resp])
        dept = await Department.filter(id=param['dept_id']).first().values()

        param['index'] = dept_job_resp_index + 1
        param['code'] = f"PL{dept['pinyin']}{param['index']:02d}"
        return param

    @classmethod
    async def after_create(cls, data):
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
            job_resp = await JobResp.filter(id=item['job_resp_id']).first().values()
            per_goal = await PerGoal.filter(id=item['per_goal_id']).first().values()
            item['job_resp_code'] = job_resp['code']
            item['job_resp_abst'] = job_resp['abstract']
            item['per_goal_code'] = per_goal['code']
            item['dept_name'] = dept_list[item['dept_id']]

            item['requester_name'] = user_list[item['requester']]

            item['applicant_tag'] = group_list[item['applicant_id']] if item['applicant_id'] else None

        return data

    @classmethod
    async def before_update(cls, request, param, data):
        if 'carry_out' in param:
            param['carry_out'] = param['carry_out'] in ['true', 'True', '1', '1']
        return param

    @classmethod
    async def after_update(cls, data):
        return data


module_workplan.router_list([
    ('', WorkPlanService.Create),
    ('', WorkPlanService.Select),
    ('/<id:int>', WorkPlanService.SelectIn),
    ('/approve/<id:str>', WorkPlanService.Vetting),
    ('/<id:str>', WorkPlanService.Update),
    ('/<id:str>', WorkPlanService.Delete),
    ('/<name:str>/<value>', WorkPlanService.SelectBy)
])
