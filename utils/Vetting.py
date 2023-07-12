from utils.BaseView import BaseView
from utils.Now import now, Now


def vetting(cls):
    pk_name = cls.Model._meta.pk_attr

    class Vetting(BaseView):
        async def put(self, request, id: any):
            __data__ = await cls.Model.filter(**{pk_name: id}).first()
            if not __data__:
                return self.error('ID不存在')
            param = {}

            for item in ['status']:
                param[item] = request.form.get(item)
            if param['status'] in ['0', 0]:
                param['refuse_reason'] = None
                param['request_time'] = None
                param['approve_time'] = None
            elif param['status'] in ['1', 1]:
                param['request_time'] = Now()
                param['approve_time'] = None
            elif param['status'] in ['2', 2, '3', 3]:
                param['approve_time'] = Now()
                if param['status'] in [2, '2']:
                    param['refuse_reason'] = None
                else:
                    param['refuse_reason'] = request.form.get('refuse_reason')
                    if param['refuse_reason'].strip() == '':
                        raise ValueError('驳回原因不得为空')

            await __data__.update_from_dict(param)
            await __data__.save()

            return self.success()

    cls.Vetting = Vetting
    return cls
