from tortoise.expressions import Q

from utils.BaseView import BaseView


def crud(cls):
    fields_list = cls.Model._meta.fields

    class Create(BaseView):
        async def post(self, request):
            """"""
            param = {}
            for item in fields_list:
                if item in request.form:
                    param[item] = request.form.get(item)

            if hasattr(cls, 'before_create'):
                param = await cls.before_create(request, param)
            __data__ = cls.Model(**param)
            await __data__.save()
            __data__ = dict(__data__)
            if hasattr(cls, 'after_create'):
                __data__ = await cls.after_create(__data__)
            return self.success(data=__data__)

    class SelectBy(BaseView):
        async def get(self, request, name: str, value):
            """"""
            if name not in fields_list:
                return self.error('字段不存在')
            data = await cls.Model.filter(**{name: value}).values()
            ############
            self.sort(data, request, cls.Model._meta.pk_attr)
            ############
            data, page_info = self.paginate(data, request)
            ############
            if hasattr(cls, 'after_select'):
                data = await cls.after_select(data)

            return self.success(data=data, page_info=page_info)

    class Select(BaseView):
        async def get(self, request):
            """"""
            keyword = request.form.get('keyword', 'all')

            data = []
            if keyword == 'all':
                data = await cls.Model.all().values()
            else:
                condition = None
                for item in fields_list:
                    __condition__ = Q(**{"{}__contains".format(item): keyword})
                    if condition is None:
                        condition = __condition__
                    else:
                        condition |= __condition__
                data = await cls.Model.filter(condition).values()

            ############
            self.sort(data, request, cls.Model._meta.pk_attr)
            ############

            data, page_info = self.paginate(data, request)
            ############
            if hasattr(cls, 'after_select'):
                data = await cls.after_select(data)

            return self.success(data=data, page_info=page_info)

    class Update(BaseView):
        async def put(self, request, id):
            """"""
            __data__ = await cls.Model.filter(id=id).first()
            if not __data__:
                return self.error('ID不存在')

            condition = {}
            for item in fields_list:
                if item in request.POST:
                    if request.POST.get(item) != __data__.__getattribute__(item):
                        condition[item] = request.POST.get(item)
            if hasattr(cls, 'before_update'):
                condition = await cls.before_update(request, condition, __data__)
            if condition:
                await __data__.update_from_dict(**condition)
                await __data__.save()
            if hasattr(cls, 'after_update'):
                __data__ = dict(__data__)
                __data__ = cls.after_update(__data__)
            return self.success(data=__data__)

    class Delete(BaseView):
        async def delete(self, request, id):
            """"""
            if id == '-1' or id == -1:
                return self.error('非法操作')
            else:
                await cls.Model.filter(pk=id).delete()
                if hasattr(cls, 'after_delete'):
                    await cls.after_delete(request, id)
                return self.success()

    cls.Create = Create
    cls.Select = Select
    cls.SelectBy = SelectBy
    cls.Update = Update
    cls.Delete = Delete

    return cls
