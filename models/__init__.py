from tortoise.models import Model

from utils.ORM import fields


class EcoClassModel(Model):
    # id = fields.IntField(primary_key=True)
    classify = fields.CharField(max_length=5)
    kind = fields.CharField(max_length=3, null=True)
    name = fields.TextField()
    comm = fields.TextField(null=True)


class Vetting(Model):
    # id = fields.IntField(primary_key=True)
    requester = fields.CharField(max_length=16, null=True, default=None)
    # 0: 待申请、1：待审批、2：通过、3：驳回（可重新申请）、4：禁止申请
    status = fields.IntField(default=0)
    refuse_reason = fields.TextField(null=True)
    request_time = fields.DatetimeField(null=True)
    approve_time = fields.DatetimeField(null=True)

    applicant_id = fields.IntField(null=True)

    class Meta:
        abstract = True


class VetGroup(Model):
    # id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=64)
    detail = fields.TextField(null=True)


class Vetter(Model):
    # id = fields.IntField(primary_key=True)
    group_id = fields.IntField()
    expert_id = fields.CharField(max_length=16)


# Create your models here.
class JobResp(Vetting):
    # id RE
    code = fields.CharField(max_length=64)
    index = fields.IntField()
    dept_id = fields.IntField()
    abstract = fields.TextField()
    detail = fields.TextField()
    operator_id = fields.CharField(max_length=64)
    leader_id = fields.CharField(max_length=64)
    comm = fields.TextField(null=True)


class PerGoal(Vetting):
    # PE
    # id = fields.IntField()
    code = fields.CharField(max_length=64)
    index = fields.IntField()
    dept_id = fields.IntField()
    quota_1 = fields.TextField()
    quota_2 = fields.TextField()
    quota_3 = fields.TextField()
    quota_value = fields.TextField()
    source = fields.TextField()
    comm = fields.TextField(null=True)


class WorkPlan(Vetting):
    # PL
    # id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=64, pk=True)
    index = fields.IntField()
    dept_id = fields.IntField()
    name = fields.TextField()
    detail = fields.TextField()
    job_resp_id = fields.IntField()
    per_goal_id = fields.IntField()
    carry_out = fields.BooleanField()
    comm = fields.TextField(null=True)


class PlanList(Vetting):
    # PW
    # id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=64, pk=True)
    index = fields.IntField()
    dept_id = fields.IntField()
    eco_class_id = fields.IntField()
    detail = fields.TextField()  # 业务经济内容
    start_date = fields.DateField()
    content = fields.TextField()
    annual_work_plan_id = fields.CharField(max_length=64)
    carry_out = fields.BooleanField()
    comm = fields.TextField(null=True)


class Budget(Vetting):
    # id
    economy_id = fields.IntField()
    budget_price = fields.DecimalField(max_digits=14, decimal_places=2)
    aebp_id = fields.CharField(max_length=16)
    detail = fields.TextField()
    actual_cost = fields.DecimalField(max_digits=14, decimal_places=2)
    diff_reason = fields.TextField(null=True)
    comm = fields.TextField(null=True)


class Department(Model):
    # id = fields.IntField(primary_key=True)
    name = fields.TextField()
    pinyin = fields.CharField(max_length=32)
    detail = fields.TextField(null=True)


class Employee(Model):
    id = fields.CharField(max_length=16, pk=True)
    name = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    pro_title = fields.CharField(max_length=64)
    job_title = fields.CharField(max_length=64)
    dept_id = fields.IntField()
    """
    client
    expert
    finance
    admin
    """
    usertype = fields.TextField()
    comm = fields.TextField(null=True)


class File(Model):
    id = fields.UUIDField(pk=True)
    per_goal_id = fields.IntField()
    name = fields.TextField()
    ext = fields.CharField(max_length=8)


class TeachInfo(Model):
    # id = auto
    dept_id = fields.IntField()
    year = fields.IntField()
    major_num = fields.IntField(default=0)
    province_key_discipline_num = fields.IntField(default=0)
    undergraduate_num = fields.IntField(default=0)
    province_first_class_course_num = fields.IntField()
    province_first_class_major_num = fields.IntField(default=0)
    nation_first_class_major_num = fields.IntField(default=0)
    nation_first_class_course_num = fields.IntField(default=0)
    province_teach_reward = fields.TextField(null=True)
    top_reward_num = fields.IntField(default=0)
    comm = fields.TextField(null=True)


class ResearchInfo(Model):
    # id = auto
    dept_id = fields.IntField()
    year = fields.IntField()
    province_research_num = fields.IntField(default=0)
    province_research_fund = fields.DecimalField(max_digits=14, decimal_places=4)
    province_key_lab_num = fields.IntField(default=0)
    province_reward_num = fields.IntField(default=0)
    nation_research_num = fields.IntField(default=0)
    nation_research_fund = fields.DecimalField(max_digits=14, decimal_places=4)
    nation_key_lab_num = fields.IntField(default=0)
    nation_reward_num = fields.IntField(default=0)
    fund_total = fields.DecimalField(max_digits=14, decimal_places=4)
    comm = fields.TextField(null=True)
