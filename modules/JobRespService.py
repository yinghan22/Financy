"""
@file    : JobResponseService.py
@author  : zhufengshuo/朱凤硕
@email   : 2257956934@qq.com
@create  : 2023/05/03 17:16
"""

from models import JobResp, Department, Employee, VetGroup
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
        if not param['worker'] or param['worker'] == '':
            raise ValueError('请输入经办人')
        if not param['leader'] or param['leader'] == '':
            raise ValueError('请输入责任领导')
        if not param['content'] or param['content'].strip() == '':
            raise ValueError('请输入工作职责内容')

        dept_job_resp = await cls.Model.filter(dept_id=param['dept_id']).values()
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
            group_list[item['id']] = item['name']

        dept_temp = await Department.all().values()
        dept_list = {}
        for item in dept_temp:
            dept_list[item['id']] = item['name']

        for item in data:
            item['leader_name'] = user_list[item['leader']]
            item['worker_name'] = user_list[item['worker']]

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


module_job_resp.router_list([
    ('/', JobRespService.Select),
    ('/', JobRespService.Create),
    ('/vet/<id:int>', JobRespService.Vetting),
    ('/<id:int>', JobRespService.Update),
    ('/<id:int>', JobRespService.Delete),
    ('/<name:str>/<value>', JobRespService.SelectBy)
])
