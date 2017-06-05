# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError



class plan_return(models.TransientModel):
    """
        返回
    """
    _name = "employees_growth.plan_return"
    _description = "Plan return"

    return_reason = fields.Text("Return reason", help="Return reason")


    @api.multi
    def pendingAudit_return_wizard(self):
        """
            退回重做：
                1、获取备注信息
                2、备注数据传递给主记录
        :return:
        """
        context = dict(self._context or {})
        active_id = context.get('active_id', '') or ''
        record = self.env['employees_growth.training_plan'].browse(active_id)
        if record.state not in ('pendingAudit',):
            raise UserError(_("The selected document is not pending status."))
        record.pendingAudit_to_draft(self.return_reason)
        return {'type': 'ir.actions.act_window_close'}