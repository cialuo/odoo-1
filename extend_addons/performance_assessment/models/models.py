# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

from odoo.exceptions import ValidationError

class CheckingIndicator(models.Model):
    """
    考核指标库
    """
    _name = "performance.indicator"

    _sql_constraints = [('indicator code unique', 'unique (indicatorcode)', 'indicator code Can not duplication')]

    # 编号
    indicatorcode = fields.Char(string='indicator code', required=True)

    # 指标名称
    name = fields.Char(string="indicator name", required=True)

    # 创建人
    creator = fields.Many2one('res.users',string="creator", default=lambda self: self._uid)

    # 创建时间
    create_date = fields.Datetime(string="create time")

    # 指标类型
    indicatortype = fields.Char(string="indicator type")

    # 最高分
    highestscore = fields.Float(string="highest score")

    # 最低分
    lowest_score = fields.Float(string="lowest score")

    # 评分标准
    standardofgrading = fields.Text(string="standard of grading")



class IndicatorForTable(models.Model):
    """
    考核表指标
    """
    _name = "performance.indecatorfortable"

    # 关联的考核表
    table_id = fields.Many2one("performance.checkingtable", string="checking table", ondelete="cascade")

    # 权重
    weight = fields.Integer("indicator weight(%)", required=True)

    # 评价人
    judge = fields.Many2many("hr.employee", string="checking judge")

    # 关联指标
    indicator_id = fields.Many2one("performance.indicator", string="indicator", required=True)

    # 指标编码
    indicator_code = fields.Char(string="indecator code", related="indicator_id.indicatorcode", readonly=True)

    # 指标名称
    indicator_name = fields.Char(string="indecator name", related="indicator_id.name", readonly=True)

    # 指标标准
    indicator_standardofgrading = fields.Text(string="indecator standardofgrading", related="indicator_id.standardofgrading", readonly=True)



class CheckingTable(models.Model):

    """
    考核表
    """
    _name = "performance.checkingtable"

    _sql_constraints = [('table code  unique', 'unique (tablecode)', 'table code Can not duplication')]

    # 考核表编码
    tablecode = fields.Char(string="checking table code", required=True)

    # 考核表名
    name = fields.Char(string="checking table name", required=True)

    # 部门
    department_id = fields.Many2one("hr.department", string="department")

    # 岗位
    post_id = fields.Many2one("employees.post", string="post")

    # 创建人
    creator = fields.Many2one('res.users', string="creator", default=lambda self: self._uid)

    # 周期类型
    cycletype = fields.Selection([("month", "month"),           # 月度
                                  ("quarter", "quarter"),       # 季度
                                  ("halfyear", "halfyear"),     # 半年
                                  ("year", "year"),             # 一年
                                  ], string="cycle type")

    # 考核指标
    indicators = fields.One2many("performance.indecatorfortable", 'table_id', string="checking indicators")

    # 创建时间
    create_date = fields.Datetime(string="create time")

    def _vailidateWeight(self, indicators):
        count = 0
        for item in indicators:
            count += item.weight
        if count != 100:
            raise ValidationError(_("weight count must be 100"))

    @api.multi
    def write(self, vals):
        result = super(CheckingTable, self).write(vals)
        self._vailidateWeight(self.indicators)
        return result

    @api.model
    def create(self, vals):
        result = super(CheckingTable, self).create(vals)
        self._vailidateWeight(result.indicators)
        return result


class PerformanceChecking(models.Model):
    """
    考核管理
    """
    _name = "perf.checking"

    _rec_name = "checkingcode"

    _sql_constraints = [('checking code  unique', 'unique (checkingcode)', 'checking code Can not duplication')]

    # 编码
    checkingcode  = fields.Char(string="checking code", required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 计划完成时间
    plandonetime = fields.Date(string="plan done time", required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 创建人
    creator = fields.Many2one('res.users', string="creator", default=lambda self: self._uid)

    # 考核表
    table_id = fields.Many2one("performance.checkingtable", string="checking table", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 周期类型
    cycletype = fields.Selection([("month", "month"),       # 月度
                                  ("quarter", "quarter"),   # 季度
                                  ("halfyear", "halfyear"), # 半年
                                  ("year", "year"),         # 一年
                                  ], string="cycle type", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 考核周期
    checkingcycle = fields.Char(string="checking cycle", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 创建时间
    create_date = fields.Datetime(string="create time")

    # 考核指标
    indicators = fields.One2many("perf.indi_check", 'checking_id', string="checking indicators", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 状态
    state = fields.Selection([("draft", "draft"),                   # 草稿
                              ("cheking", "cheking on the way"),    # 审批中
                              ("done", "checking done"),            # 完成
                              ], default='draft', string="checking status")

    # 考核员工
    employees = fields.Many2many("hr.employee", string="employees to checking", readonly=True,
                                  states={'draft': [('readonly', False)]})

    # 部门
    department_id = fields.Many2one(string="department", related="table_id.department_id")

    # 岗位
    post_id = fields.Many2one(string="post", related="table_id.post_id")

    # 备注
    remark = fields.Text(string="checking remarks")

    def _vailidateWeight(self, indicators):
        count = 0
        for item in indicators:
            count += item.weight
        if count != 100:
            raise ValidationError(_("weight count must be 100"))


    @api.onchange("table_id")
    def reuildIndicatorinfo(self):
        self.cycletype = self.table_id.cycletype
        if self.table_id.indicators:
            data = []
            for detail in self.table_id.indicators:
                vals = {
                    "checking_id": self.id,
                    "weight": detail.weight,
                    "indicator_id": detail.indicator_id,
                }
                judge = []
                for itme in detail.judge:
                    judge.append((4,itme.id, _))
                vals['judge'] = judge
                data.append((0, 0, vals))
            self.indicators = data

    @api.multi
    def action_checking(self):
        resultmodel = self.env['perf.checkingresult']
        for item in self.employees:
            data = {
                'checking_id':self.id,
                'employee_id':item.id,
                'name':self.table_id.name,
            }
            indis = []
            for indicator in self.indicators:
                indis.append((0, 0, {'indicator_id': indicator.id, 'point': 0}))
            data['indicators'] = indis
            resultmodel.create(data)
        self.state = 'cheking'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def write(self, vals):
        result = super(PerformanceChecking, self).write(vals)
        self._vailidateWeight(self.indicators)
        return result

    @api.model
    def create(self, vals):
        result = super(PerformanceChecking, self).create(vals)
        self._vailidateWeight(result.indicators)
        return result

class IndicatorForChecking(models.Model):
    """
    考核指标
    """
    _name = "perf.indi_check"

    # 关联的考核表
    checking_id = fields.Many2one("perf.checking", string="checking plan", ondelete="cascade")

    # 权重
    weight = fields.Integer("indicator weight(%)", required=True)

    # 评价人
    judge = fields.Many2many("hr.employee", string="checking judge")

    # 关联指标
    indicator_id = fields.Many2one("performance.indicator", string="indicator", required=True)

    # 指标编码
    indicator_code = fields.Char(string="indecator code", related="indicator_id.indicatorcode", readonly=True)

    # 指标名称
    indicator_name = fields.Char(string="indecator name", related="indicator_id.name", readonly=True)

    # 指标标准
    indicator_standardofgrading = fields.Text(string="indecator standardofgrading", related="indicator_id.standardofgrading", readonly=True)


class CheckingResult(models.Model):

    _name = "perf.checkingresult"

    # 关联的考核表
    checking_id = fields.Many2one("perf.checking", string="checking plan", ondelete="cascade")

    # 考核名称
    name = fields.Char(string="checking name")

    # 员工
    employee_id = fields.Many2one("hr.employee", string="employee")

    # 编码
    checkingcode = fields.Char(string="checking code", related="checking_id.checkingcode")

    # 周期类型
    cycletype = fields.Selection(string="cycle type", related="checking_id.cycletype")

    # 考核周期
    checkingcycle = fields.Char(string="checking cycle", related="checking_id.checkingcycle")

    # 考核指标
    indicators = fields.One2many("perf.resultindicator", 'result_id', string="checking indicators")

    # 部门
    department_id = fields.Many2one(string="department", related="checking_id.department_id")

    # 岗位
    post_id = fields.Many2one(string="post", related="checking_id.post_id")

    # 状态
    state = fields.Selection([("checking", "checking on the way"),      # 考核总
                              ("checkingdone", "checking done"),        # 考核完成
                              ], default='checking', string="checking status")

    # 考核结果总分
    totalpoint = fields.Float(string="checking total point", compute="_computeTotalPoint")

    @api.multi
    def _computeTotalPoint(self):
        for item in self:
            total = 0
            for point in item.indicators:
                total += point.point
            item.totalpoint = total

    @api.multi
    def action_done(self):
        self.state = 'checkingdone'



class CheckingResultIndicator(models.Model):

    _name = "perf.resultindicator"

    # 关联的考核结果
    result_id = fields.Many2one("perf.checkingresult", string="checking result")

    # 评分
    point = fields.Float(string="result point", required=True)

    # 关联指标
    indicator_id = fields.Many2one("perf.indi_check", string="indicator", required=True)

    # 指标编码
    indicator_code = fields.Char(string="indecator code", related="indicator_id.indicator_code", readonly=True)

    # 指标名称
    indicator_name = fields.Char(string="indecator name", related="indicator_id.indicator_name", readonly=True)

    # 指标标准
    indicator_standardofgrading = fields.Text(string="indecator standardofgrading",
                                              related="indicator_id.indicator_standardofgrading", readonly=True)

    # 评价人
    judge = fields.Many2many(string="checking judge", related="indicator_id.judge")

    @api.one
    @api.constrains('point')
    def _check_description(self):
        if self.point > self.indicator_id.indicator_id.highestscore:
            raise ValidationError(_("point must less then highest score"))

        if self.point < self.indicator_id.indicator_id.lowest_score:
            raise ValidationError(_("point must higher then lowest score"))
