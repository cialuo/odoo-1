# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError


class GenBusMoveTime(models.TransientModel):
    _name = 'genbusmovetime'

    rule_id = fields.Many2one('scheduleplan.schedulrule', 'rule id', required=True)

    use_date = fields.Date(default=fields.Date.context_today, string="target date")

    @api.model
    def default_get(self, fields):
        res = super(GenBusMoveTime, self).default_get(fields)
        res['rule_id'] = self.env.context.get('active_id')
        return res

    @api.multi
    def gendata(self):
        check_type_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # 检查生成线路的日期与日期类型是否匹配
        if self.rule_id.date_type.type in check_type_list:
            # 计算 self.use_date 是该周的第几天
            weekday = datetime.datetime.strptime(self.use_date, '%Y-%m-%d').weekday()

            # 如果生成线路的日期对应的星期与日期类型不匹配，前端提示异常消息
            if check_type_list[weekday] != self.rule_id.date_type.type:
                raise UserError(('生成线路的日期与日期类型不匹配.'))

        res = self.rule_id.createMoveTimeRecord(self.use_date, self.rule_id)
        res.genOperatorPlan()
        self.env['bus_staff_group'].action_gen_staff_group(res.line_id,
                                                           staff_date=datetime.datetime.strptime(
                                                               res.executedate, "%Y-%m-%d"),
                                                           operation_ct=res.vehiclenums,
                                                           move_time_id=res,
                                                           force=True)
        self.env['scheduleplan.schedulrule'].genExcuteRecords(res)
        return