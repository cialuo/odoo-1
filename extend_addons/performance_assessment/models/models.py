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
    table_id = fields.Many2one("performance.checkingtable", string="checking table")

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
    indicator_standardofgrading = fields.Char(string="indecator code", related="indicator_id.indicatorcode", readonly=True)



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
            count = item.weight
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
