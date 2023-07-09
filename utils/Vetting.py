from utils.BaseView import BaseView
from utils.Now import now


def vetting(cls):
    class Vetting(BaseView):
        async def post(self, request, id):
            __data__ = await cls.Model.filter(id=id).first()
            if not __data__:
                return self.error('ID不存在')
            param = {}
            term = 0
            if __data__.vet_3 is None:
                term = 2
            elif __data__.vet_2 is None:
                term = 1

            for item in ['applicant', 'vetting_status', 'refuse_reason', 'apply_time', 'vetting_time', 'vet_1', 'vet_2',
                         'vet_3']:
                param[item] = request.form.get(item)
            if param['vetting_status'] in ['0', 0]:
                param['refuse_reason'] = ''
                param['apply_time'] = None
                param['vetting_time'] = None
                param['vet_1'] = None
                param['vet_2'] = None
                param['vet_3'] = None
            elif param['vetting_status'] in ['1', 1]:
                param['apply_time'] = now()
                param['vetting_time'] = None
            elif param['vetting_status'] in ['2', 2, '3', 3]:
                param['vetting_time'] = now()
                if param['vetting_status'] in [2, '2']:
                    param['refuse_reason'] = None
                elif param['refuse_reason'].strip() == '':
                    raise ValueError('驳回原因不得为空')

            if __data__.vetting_status in ['4', 4]:
                raise ValueError('当前已禁止重新申请审批')

            return param

    cls.Vetting = Vetting
    return cls
