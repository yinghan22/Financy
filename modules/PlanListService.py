from models import PlanList, Department, VetGroup, Employee, EcoClassModel, WorkPlan
from utils.CRUD import crud
from utils.Module import Module

module_planlist = Module('planlist', url_prefix='/api/planlist')


@crud
class PlanListService:
    Model = PlanList

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')
        dept_plan_list = await cls.Model.filter(dept_id=param['dept_id']).values()
        dept_plan_list_index = max([item['index'] for item in dept_plan_list])
        param['index'] = dept_plan_list_index + 1
        dept = await Department.filter(id=param['dept_id']).first().values()
        param['code'] = f"PW{dept['pinyin']}{param['index']:02d}"
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
            group_list[item['id']] = item['name']
        dept_temp = await Department.all().values()
        dept_list = {}
        for item in dept_temp:
            dept_list[item['id']] = item['name']

        eco_class_temp = await EcoClassModel.all().values()
        eco_class_list = {}
        for item in eco_class_temp:
            eco_class_list[str(item['id'])] = item['name']

        for item in data:

            item['dept_name'] = dept_list[item['dept_id']]
            item['eco_class_name'] = eco_class_list[item['eco_class_id']]
            item['work_plan_code'] = await WorkPlan.filter(work_plan_id=item['work_plan_id']).first().values()['code']

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
    async def before_update(cls, request, param, data):
        return param

    @classmethod
    async def after_update(cls, data):
        return None


module_planlist.router_list([
    ('', PlanListService.Create),
    ('', PlanListService.Select),
    ('/<id:int>', PlanListService.Update),
    ('/<id:int>', PlanListService.Delete),
    ('/<name:str>/<value>', PlanListService.SelectBy)
])
