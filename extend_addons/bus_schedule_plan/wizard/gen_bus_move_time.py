# -*- coding:utf-8 -*-

from odoo import api, fields, models, _

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
        return