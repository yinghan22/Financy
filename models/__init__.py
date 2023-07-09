from tortoise.models import Model

from utils.ORM import fields


class EcoClassModel(Model):
    # id = fields.IntField(primary_key=True)
    class_id = fields.CharField(max_length=5)
    kind_id = fields.CharField(max_length=3, null=True)
    name = fields.TextField()
    description = fields.TextField(null=True)


class Vetting(Model):
    # id = fields.IntField(primary_key=True)
    applicant = fields.IntField(null=True, default=None)
    # 0: 待申请、1：待审批、2：通过、3：驳回（可重新申请）、4：禁止申请
    vetting_status = fields.IntField(default=0)
    refuse_reason = fields.TextField(null=True)
    apply_time = fields.DatetimeField(null=True)
    vetting_time = fields.DatetimeField(null=True)

    vet_1 = fields.IntField(null=True)
    vet_2 = fields.IntField(null=True)
    vet_3 = fields.IntField(null=True)

    class Meta:
        abstract = True


class VetGroup(Model):
    # id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=64)
    comm = fields.TextField(null=True)


class Vetter(Model):
    # id = fields.IntField(primary_key=True)
    group_id = fields.IntField()
    user_id = fields.IntField()


# Create your models here.
class JobResp(Vetting):
    # id RE
    code = fields.CharField(max_length=64)
    index = fields.IntField()
    dept_id = fields.IntField()
    abstract = fields.TextField()
    content = fields.TextField()
    worker = fields.IntField()
    leader = fields.IntField()
    comm = fields.TextField(null=True)


class PerGoal(Vetting):
    # PE
    # id = fields.IntField()
    code = fields.CharField(max_length=64)
    index = fields.IntField()
    dept_id = fields.IntField()
    goal_1 = fields.TextField()
    goal_2 = fields.TextField()
    goal_3 = fields.TextField()
    value = fields.TextField()
    source = fields.TextField()
    comm = fields.TextField(null=True)


class WorkPlan(Vetting):
    # PL
    # id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=64)
    index = fields.IntField()
    dept_id = fields.IntField()
    name = fields.TextField()
    content = fields.TextField()
    job_resp_id = fields.IntField()
    per_goal_id = fields.IntField()
    carried = fields.IntField()
    comm = fields.TextField(null=True)


class PlanList(Vetting):
    # PW
    # id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=64, pk=True)
    index = fields.IntField()
    dept_id = fields.IntField()
    eco_class_id = fields.IntField()
    year_mon = fields.DateField()
    content = fields.TextField()
    work_plan_id = fields.IntField()
    carried = fields.IntField()
    comm = fields.TextField(null=True)


class Budget(Vetting):
    # id
    eco_class_id = fields.IntField()
    budget = fields.DecimalField(max_digits=14, decimal_places=2)
    dept_id = fields.IntField()
    plan_list_id = fields.IntField()
    detail = fields.TextField()
    actual_cost = fields.DecimalField(max_digits=14, decimal_places=2)
    diff_reason = fields.TextField(null=True)
    comm = fields.TextField(null=True)


class Department(Model):
    # id = fields.IntField(primary_key=True)
    name = fields.TextField()
    pinyin = fields.CharField(max_length=32)
    comm = fields.TextField(null=True)


class Employee(Model):
    # id = fields.IntField(primary_key=True)
    work_id = fields.CharField(max_length=16)
    name = fields.CharField(max_length=64)
    password = fields.CharField(max_length=128)
    pro_title = fields.CharField(max_length=64)
    job_title = fields.CharField(max_length=64)
    dept_id = fields.IntField()
    """
    0 employee
    1 expert
    2 finance
    9 admin
    """
    usertype = fields.IntField()
    comm = fields.TextField(null=True)


class File(Model):
    id = fields.UUIDField(pk=True)
    per_goal_id = fields.IntField()
    filename = fields.TextField()
    uploader = fields.IntField()
    upload_time = fields.DatetimeField()
    ext = fields.CharField(max_length=8)


class TeachInfo(Model):
    # id = auto
    dept_id = fields.IntField()
    year = fields.TextField()
    major_num = fields.IntField(default=0)
    province_key_course_num = fields.IntField(default=0)
    under_num = fields.IntField(default=0)
    province_course_num = fields.IntField()
    province_major_num = fields.IntField(default=0)
    nation_course_num = fields.IntField(default=0)
    nation_major_num = fields.IntField(default=0)
    reward = fields.TextField(default=0)
    reward_num = fields.IntField(default=0)
    comm = fields.TextField(null=True)


class ResearchInfo(Model):
    # id = auto
    dept_id = fields.IntField()
    year = fields.TextField()
    province_research_num = fields.IntField(default=0)
    province_budget = fields.DecimalField(max_digits=14, decimal_places=4)
    province_key_lab_num = fields.IntField(default=0)
    province_reward_num = fields.IntField(default=0)
    nation_research_num = fields.IntField(default=0)
    nation_budget = fields.DecimalField(max_digits=14, decimal_places=4)
    nation_key_lab_num = fields.IntField(default=0)
    nation_reward_num = fields.IntField(default=0)
    budget_total = fields.DecimalField(max_digits=14, decimal_places=4)
    comm = fields.TextField(null=True)
