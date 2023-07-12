"""
@file    : JobResponseService.py
@author  : zhufengshuo/朱凤硕
@email   : 2257956934@qq.com
@create  : 2023/05/03 17:16
"""

from models import JobResp, Department, Employee, VetGroup, Vetter
from utils.CRUD import crud
from utils.Module import Module
from utils.Vetting import vetting

module_job_resp = Module('job', url_prefix='/api/job')


@crud
@vetting
class JobRespService:
    Model = JobResp

    @classmethod
    async def before_create(cls, request, param):
        if not param['dept_id'] or param['dept_id'] == '':
            raise ValueError('请输入教研室/部门/科室')
        if not param['operator_id'] or param['operator_id'] == '':
            raise ValueError('请输入经办人')
        if not param['leader_id'] or param['leader_id'] == '':
            raise ValueError('请输入责任领导')
        if not param['detail'] or param['detail'].strip() == '':
            raise ValueError('请输入工作职责内容')

        dept_job_resp = await cls.Model.filter(dept_id=param['dept_id']).values()
        dept_job_resp_index = 0
        if len(dept_job_resp):
            dept_job_resp_index = max([item['index'] for item in dept_job_resp])
        param['index'] = dept_job_resp_index + 1
        dept = await Department.filter(id=param['dept_id']).first().values()

        param['code'] = f"RE{dept['pinyin']}{param['index']:02d}"
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
            item['dept_name'] = dept_list[item['dept_id']]
            item['requester'] = str(item['requester'])
            item['requester_name'] = user_list[item['requester']]
            item['operator_name'] = user_list[item['operator_id']]

            item['leader_name'] = user_list[item['leader_id']]
            item['applicant_tag'] = group_list[item['applicant_id']] if item['applicant_id'] else None

        return data

    @classmethod
    async def after_update(cls, data):
        return None


module_job_resp.router_list([
    ('', JobRespService.Select),
    ('', JobRespService.Create),
    ('/<id:int>', JobRespService.SelectIn),
    ('/approve/<id:int>', JobRespService.Vetting),
    ('/<id:int>', JobRespService.Update),
    ('/<id:int>', JobRespService.Delete),
    ('/<name:str>/<value>', JobRespService.SelectBy)
])
