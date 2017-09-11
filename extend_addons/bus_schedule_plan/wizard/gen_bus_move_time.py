# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
import datetime

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
        res = self.rule_id.createMoveTimeRecord(self.use_date,self.rule_id)
        res.genOperatorPlan()
        self.env['bus_staff_group'].action_gen_staff_group(res.line_id,
                                                           staff_date=datetime.datetime.strptime(
                                                               res.executedate, "%Y-%m-%d"),
                                                           operation_ct=res.vehiclenums,
                                                           move_time_id=res,
                                                           force=True)
        self.env['scheduleplan.schedulrule'].genExcuteRecords(res)
        return