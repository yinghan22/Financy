"""
@file    : UserService.py
@author  : yingHan/嬴寒
@email   : yinghan22@163.com
@create  : 2023/4/30 下午5:07
"""
import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256

import Config
from models import Employee as Model, Department, Employee, Vetter, VetGroup
from utils.BaseView import BaseView
from utils.CRUD import crud
from utils.Module import Module

module_user = Module('user', url_prefix='/api/user')

department_list = {}


@crud
class UserService:
    Model = Employee

    @classmethod
    async def after_select(cls, data):
        dept_temp = await Department.all().values()
        for item in dept_temp:
            department_list[str(item['id'])] = item['name']

        for item in data:
            item['dept_name'] = department_list[str(item['dept_id'])]
            del item['password']
        return data

    @classmethod
    async def before_create(cls, request, param):
        confirm = request.form.get('confirm', '').strip()
        for item in ['id', 'name', 'password', 'usertype', 'job_title']:
            if param[item] == '':
                raise ValueError(f"参数错误 {item} 不得为空")
        if confirm != param['password']:
            raise ValueError('两次输入密码不一致')
        if param['dept_id'] == '':
            param['dept_id'] = None
        param['password'] = pbkdf2_sha256.hash(confirm)
        __data__ = await cls.Model.filter(id=param['id']).exists()
        if __data__:
            raise ValueError('当前工号已存在')
        return param

    @classmethod
    async def after_create(cls, data):
        return None

    @classmethod
    async def before_update(cls, request, param, data):
        if 'password' in param:
            raise ValueError('请使用重置密码以更换密码')
        return param

    @classmethod
    async def after_update(cls, data):
        return None

    class ResetPassword(BaseView):
        """重置密码"""

        async def put(self, request, id: str):
            __data__ = await Model.filter(id=id).first()
            if not __data__:
                return self.error(f"用户id为：{id}不存在")
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm', '').strip()
            if password == '':
                return self.error('请输入密码')
            elif password != confirm:
                return self.error('两次输入的密码不一致')
            __data__.password = pbkdf2_sha256.hash(confirm)
            await __data__.save()
            return self.success(message='success')

    class ChangePassword(BaseView):
        """修改密码"""

        async def put(self, request, id: str):
            __data__ = await Model.filter(id=id).first()
            if not __data__:
                return self.error(f"用户id为：{id}不存在")
            old_password = request.form.get('old_password', '').strip()
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm', '').strip()
            if old_password == '':
                return self.error(message='请输入旧密码')
            elif password == '':
                return self.error('请输入密码')
            elif password == old_password:
                return self.error('新密码不得与旧密码一致')
            elif password != confirm:
                return self.error('两次输入的密码不一致')
            elif not pbkdf2_sha256.verify(password, __data__.password):
                return self.error('旧密码不正确')
            __data__.password = pbkdf2_sha256.hash(password)
            await __data__.save()
            return self.success(message='success')

    class Login(BaseView):
        """登录"""

        async def post(self, request):
            id = request.form.get('id', '').strip()
            password = request.form.get('password', '').strip()
            if password == '' or id == '':
                return self.error(message='请输入工号和密码')
            __data__ = await Model.filter(id=id).first()
            if not __data__:
                return self.error(message='用户名或密码错误')
            data = dict(__data__)

            if not pbkdf2_sha256.verify(password, data['password']):
                return self.error(message='用户名或密码错误')
            del data['password']
            if data['dept_id'] not in department_list:
                department_list_temp = await Department.all().values()
                for dept in department_list_temp:
                    department_list[dept['id']] = dept['name']
            data['dept_name'] = department_list[data['dept_id']]

            belong_group = await Vetter.filter(expert_id=data['id']).values()
            all_group = await VetGroup.all().values()
            group_info = {item['id']: item for item in all_group}
            group_list = [group_info[item['group_id']] for item in belong_group]
            data['group_list'] = group_list

            response = self.success(message='success', data=data)

            token = str(uuid.uuid1().hex)

            async with request.app.ctx.redis as redis:
                __token__ = request.headers.get('X-token', '')
                await redis.delete(f"token:{__token__}")
                await redis.set(f"token:{token}", data['id'], ex=Config.Config['time']['three_day'], )
                response.headers['X-token'] = token
            return response

    class Logout(BaseView):
        async def post(self, request):
            token = request.headers.get('X-token', '')
            async with request.app.ctx.redis as redis:
                temp = await redis.get(f"token:{token}")
                if temp is None:
                    return self.success()
                else:
                    await redis.delete(f"token:{token}")
            return self.success(message='success')

    class SetPass(BaseView):
        async def post(self, request, id):
            __data__ = await Model.filter(id=id).first()
            if not __data__:
                return self.error(f"用户id为：{id}不存在")
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm', '').strip()
            if password == '':
                return self.error('请输入密码')
            elif password != confirm:
                return self.error('两次输入的密码不一致')
            __data__.password = pbkdf2_sha256.hash(password)
            await __data__.save()
            return self.success(message='success')


module_user.router_list([
    ('', UserService.Select),
    ('', UserService.Create),
    ('/<id:int>', UserService.SelectIn),
    ('/<id:int>', UserService.Update),
    ('/<id:int>', UserService.Delete),
    ('/resetpass/<id:str>', UserService.ResetPassword),
    ('/changepass/<id:str>', UserService.ChangePassword),
    ('/setpass/<id:str>', UserService.SetPass),
    ('/login', UserService.Login),
    ('/logout', UserService.Logout),
    ('/<name:str>/<value>', UserService.SelectBy)
])
