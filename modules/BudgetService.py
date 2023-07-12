from models import Budget, Employee, VetGroup, Department, EcoClassModel, Vetter
from utils.CRUD import crud
from utils.Module import Module
from utils.Vetting import vetting

module_budget = Module('budget', url_prefix='/api/budget')


@crud
@vetting
class BudgetService:
    Model = Budget

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
        eco_class_temp = await EcoClassModel.all().values()
        eco_class_list = {}
        for item in eco_class_temp:
            eco_class_list[str(item['id'])] = item['name']
        for item in data:
            item['requester_name'] = user_list[item['requester']]
            item['applicant_tag'] = group_list[item['applicant_id']] if item['applicant_id'] else None
            item['eco_class_name'] = eco_class_list[str(item['economy_id'])]
        return data

    @classmethod
    async def before_update(cls, request, param, data):
        return param

    @classmethod
    async def after_update(cls, data):
        return None


module_budget.router_list([
    ('', BudgetService.Select),
    ('', BudgetService.Create),
    ('/<id:int>', BudgetService.SelectIn),
    ('/approve/<id>', BudgetService.Vetting),
    ('/<id:int>', BudgetService.Update),
    ('/<id:int>', BudgetService.Delete),
    ('/<name:str>/<value>', BudgetService.SelectBy)
])
