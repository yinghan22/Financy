"""
@file    : TeachActivityService.py
@author  : wangxiping/王淅平
@email   : 3146453993@qqcom.com
@create  : 2023/04/30 19:16
"""
import os.path
from os import path

import aiofiles

from models import File
from utils.BaseView import BaseView
from utils.CRUD import crud
from utils.Module import Module
from utils.Now import now, _uuid

module_file = Module('file', url_prefix='/api/file')


def get_ext(filename):
    return os.path.splitext(filename)[1]


async def saveFile(per_goal_id, file_list):
    result = []
    file_dir = path.join(os.path.dirname(__file__), '..', 'static')
    for item in file_list:
        file_name = item.name
        file_ext = get_ext(file_name)
        file_id = _uuid()

        file_path = path.join(file_dir, f"{file_id}{file_ext}")
        print(file_path)
        async with aiofiles.open(file_path, 'wb') as file:
            await file.write(item.body)
        await file.close()
        param = {
            'id': file_id,
            'per_goal_id': per_goal_id,
            'name': file_name,
            'ext': file_ext
        }
        await File(**param).save()
        param['path'] = f"static/{file_id}{file_ext}"
        result.append(param)
    return result


@crud
class FileService:
    Model = File

    class Upload(BaseView):
        async def post(self, request):
            per_goal_id = request.form.get('per_goal_id')

            file_list = request.files.getlist('file_list')
            # file_ext = get_ext()

            result = await saveFile(file_list, per_goal_id)

            return self.success(data=result)

    @classmethod
    async def deleteFile(cls, per_goal_id):
        file_list = await File.filter(per_goal_id=per_goal_id).values()
        file_dir = path.join(os.path.dirname(__file__), '..', 'static')

        for item in file_list:
            file_path = path.join(file_dir, f"{item['id']}{item['ext']}")
            if path.exists(file_path):
                os.remove(file_path)

    @classmethod
    async def GetFileByPerGoalID(cls, per_goal_id):
        file_list = await File.filter(per_goal_id=per_goal_id).values()
        data = []

        for item in file_list:
            item['path'] = f"static/{item['id']}{item['ext']}"
            data.append(item)
        return data

    class DeleteFileByID(BaseView):
        async def post(self, request, id):
            file = await File.filter(id=id).first().values()
            file_dir = path.join(os.path.dirname(__file__), '..', 'static')
            file_path = path.join(file_dir, f"{file['id']}{file['ext']}")
            if path.exists(file_path):
                os.remove(file_path)
            await File.filter(id=id).delete()
            return self.success()


module_file.router_list([
    ('/upload', FileService.Upload),
    ('/<id:int>', FileService.SelectIn),
    ('/delete/<id>', FileService.DeleteFileByID),
    ('/<name:str>/<value>', FileService.SelectBy)
])
