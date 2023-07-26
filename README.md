# 环境移植

1. 下载依赖包至指定的目录

```bash
pip download -d ${dir}
```

2. 从指定目录源安装离线依赖

```bash
pip install --no-index --find-links=${dir}
```


完成情况

1. 部门
2. 经济类型
3. 人员
4. 文件
5. 审批小组
6. 审批人
7. 职责
8. 绩效
9. 工作计划
10. 计划单
11. 教学信息
12. 项目信息

# 模型分析

## 1. 经济分类科目 `eco_class`

|    字段名     |   类型   |   说明   |
| :-----------: | :------: | :------: |
|      id       | Integer  |   序号   |
|  `class_id`   | `String` |  科目类  |
|   `kind_id`   | `String` |  科目款  |
|    `name`     | `String` | 科目名称 |
| `description` | `String` |   说明   |

## 2. 部门基本信息 `dept`

| 字段名 |  类型  |    说明    |
| :----: | :----: | :--------: |
|   id   | BigInt |    序号    |
|  name  | String | 教研室名称 |
|  code  | String |    缩写    |

---

- 审批状态

|    字段名     |      类型       |                                    说明                                     |
| :-----------: | :-------------: | :-------------------------------------------------------------------------: |
|   applicant   |     Integer     |                                   申请人                                    |
|  vet_status   |     Integer     | 审批状态(0: 待申请、1：待审批、2：通过、3：驳回（可重新申请）、4：禁止申请) |
| refuse_reason |     String      |                                  驳回理由                                   |
|  apply_time   |     DateTim     |                                  申请时间                                   |
| vetting_time  |     DateTme     |                                  审批时间                                   |
|     vet_1     | Integer \| Null |                              一审审批人列表 ID                              |
|     vet_2     | Integer \| Null |                              二审审批人列表 ID                              |
|     vet_3     | Integer \| Null |                              三审审批人列表 ID                              |

- 审批分组 `gp`

| 字段名 |  类型   |    说明    |
| :----: | :-----: | :--------: |
|   id   | Integer |    序号    |
|  name  | String  | 审批组名称 |
|  comm  | String  |    备注    |

- 审批人列表

| 字段名 |  类型   |   说明    |
| :----: | :-----: | :-------: |
|   id   | Integer |   序号    |
| gp_id  | Integer | 审批组 ID |
|  uid   | Integer |  人员 ID  |

---

## 3. 人员情况表 `emploee`

|  字段名   |  类型   |    说明    |
| :-------: | :-----: | :--------: |
|    id     | Integer |    序号    |
|  work_id  | String  |    工号    |
|   name    | String  |    姓名    |
| pro_title | String  |    职称    |
| job_title | String  |    职务    |
|  dept_id  | Integer | 隶属教研室 |
|   comm    | String  |    备注    |

## 4. 工作职责 `job_resp`

`id = RE + 部门缩写 + 两位序号`

|  字段名  |  类型   |    说明    |
| :------: | :-----: | :--------: |
|    id    | String  |  职责编号  |
|  index   | Integer |    计数    |
| dept_id  | Integer | 隶属教研室 |
| abstract | String  |  职责概述  |
| content  | String  |  职责内容  |
|  worker  | Integer |   经办人   |
|  leader  | Integer |  责任领导  |
| password | String  |    密码    |
|   comm   | String  |    备注    |

## 5. 绩效目标 `per_goal`

`id = PE + 部门缩写 + 两位序号`

| 字段名  |  类型   |    说明    |
| :-----: | :-----: | :--------: |
|   id    | String  |  绩效编码  |
|  index  | Integer |    计数    |
| dept_id | Integer | 隶属教研室 |
| goal_1  | String  |  一级指标  |
| goal_2  | String  |  二级指标  |
| goal_3  | String  |  三级指标  |
|  value  | String  |   指标值   |
| source  | String  |  指标来源  |
|  comm   | String  |    备注    |

## 6. 部门年度工作计划 `work_plan`

`id = PL + 部门缩写 + 两位序号`

|   字段名    |  类型   |      说明      |
| :---------: | :-----: | :------------: |
|     id      | String  |    计划编码    |
|    index    | Integer |      计数      |
|   dept_id   | Integer |   隶属教研室   |
|    name     | String  |      名称      |
|   content   | String  |      内容      |
| job_resp_id | String  |  隶属职责编码  |
| per_goal_id | String  |  绩效目标编码  |
|   carried   | Integer | 上年度是否展开 |
|    comm     | String  |      备注      |

## 7. 部门年度经济业务计划单 `plan_list`

`id = PW + 部门缩写 + 两位序号`

|    字段名    |  类型   |      说明      |
| :----------: | :-----: | :------------: |
|      id      | String  |   业务单编码   |
|    index     | Integer |      计数      |
|   dept_id    | Integer |   隶属教研室   |
| eco_class_id | Integer |    经济分类    |
|   year_mon   |  Date   |    开展年月    |
|   content    | Srting  |  产生支出内容  |
| work_plan_id | String  |  工作计划编码  |
|   carried    | Integer | 上年度是否展开 |
|     comm     | String  |      备注      |

## 8. 公用经费预算表 `budget`

|    字段名    |     类型      |      说明      |
| :----------: | :-----------: | :------------: |
|      id      |    String     |      序号      |
| eco_class_id |    BigInt     |    经济分类    |
|    budget    | Decimal(14,2) |    预算金额    |
| plan_list_id |    String     |   计划单 ID    |
| calc_detail  |    String     |  详细测算过程  |
| actual_cost  | Decimal(14,2) | 上年度实际支出 |
| diff_reason  |    String     |    差异说明    |
|     comm     |    String     |      备注      |

## 9. 信息统计——教学活动方面（教务处填报）

|         字段名          |  类型   |              说明              |
| :---------------------: | :-----: | :----------------------------: |
|           id            | Integer |              序号              |
|          name           | String  |          教学院部名称          |
|          year           | String  |            统计年度            |
|        major_num        | Integer |            专业数量            |
| province_key_course_num | Integer |         省重点学科数量         |
|        under_num        | Integer |          本科学生人数          |
|   province_course_num   | Integer |          省一流课程数          |
|   province_major_num    | Integer |          省一流专业数          |
|    nation_course_num    | Integer |         国家一流课程数         |
|    nation_major_num     | Integer |         国家一流专业数         |
|         reward          | String  |        省以上教学成果奖        |
|       reward_num        | Integer | 教育部认可的竞赛最高获奖项目数 |
|          comm           | String  |              备注              |

## 10.

|        字段名         |     类型      |          说明          |
| :-------------------: | :-----------: | :--------------------: |
|          id           |    Integer    |          序号          |
|         name          |    String     |      教学院部名称      |
|         year          |    String     |        统计年度        |
| province_research_num |    Integer    |     省级科研项目数     |
|    province_budget    | Decimal(14,2) |  省级科研经费（万元）  |
| province_key_lab_num  |    Integer    |    省级重点实验室数    |
|  province_reward_num  |    Integer    |     省级科研获奖数     |
|  nation_research_num  |    Integer    |    国家级科研项目数    |
|     nation_budget     | Decimal(14,2) | 国家级科研经费（万元） |
|  nation_key_lan_num   |    Integer    |   国家级重点实验室数   |
|     nation_reward     |    Integer    |     国家科研获奖数     |
|     budget_total      | Decimal(14,2) |  横向科研经费（万元）  |
|         comm          |    String     |          备注          |
