from models import WorkPlan, Department, Employee, VetGroup, JobResp, PerGoal
from utils.CRUD import crud
from utils.Module import Module

module_workplan = Module('workplan', url_prefix='/api/workplan')


@crud
class WorkPlanService:
    Model = WorkPlan

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')
        dept_job_resp = await cls.Model.filter(dept_id=param['dept_id']).values()
        dept_job_resp_index = max([item['index'] for item in dept_job_resp])
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

        dept_temp = await Department.all().values()
        dept_list = {}
        for item in dept_temp:
            dept_list[item['id']] = item['name']

        for item in group_temp:
            group_list[item['id']] = item['name']
        for item in data:
            job_resp = await JobResp.filter(id=item['job_resp_id']).first().value()
            per_goal = await PerGoal.filter(id=item['per_goal_id']).first().value()
            item['job_resp_code'] = job_resp['code']
            item['job_resp_abstract'] = job_resp['abstract']
            item['per_goal_code'] = per_goal['code']
            item['dept_name'] = dept_list[item['dept_id']]

            if item['applicant']:
                item['applicant_name'] = user_list[item['applicant']]

            for index in range(1, 4):
                label = f"vet_{index}"
                if item[label]:
                    item[f"{label}_name"] = group_list[item[label]]
            if item['vet_3'] is not None:
                item['term'] = 3
            elif item['vet_2'] is not None:
                item['term'] = 2
            else:
                item['term'] = 1
        return data

    @classmethod
    async def after_update(cls, data):
        return None

    @classmethod
    async def before_update(cls, request, param, data):
        return param


module_workplan.router_list([
    ('/', WorkPlanService.Create),
    ('/', WorkPlanService.Select),
    ('/<id:int>', WorkPlanService.Update),
    ('/<id:int>', WorkPlanService.Delete),
    ('/<name:str>/<value>', WorkPlanService.SelectBy)
])
