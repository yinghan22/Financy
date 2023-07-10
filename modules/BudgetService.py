from models import Budget, Employee, VetGroup, Department, EcoClassModel
from utils.CRUD import crud
from utils.Module import Module
from utils.Vetting import vetting

module_budget = Module('budget', url_prefix='/api/budget')
@crud
@vetting
class BudgetService:
    Model = Budget

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')
        return param

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
        for item in data:

            item['dept_name'] = dept_list[item['dept_id']]
            item['eco_class_content'] = await EcoClassModel.filter(id=item['eco_class_id']).values()

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
    async def before_update(cls, request, param):
        return param

    @classmethod
    async def after_update(cls, data):
        return None
module_budget.router_list([
    ('/', BudgetService.Select),
    ('/', BudgetService.Create),
    ('/<id:int>', BudgetService.Update),
    ('/<id:int>', BudgetService.Delete),
    ('/<name:str>/<value>', BudgetService.SelectBy)
])
