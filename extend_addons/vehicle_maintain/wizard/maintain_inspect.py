# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class MaintainInspectConfirm(models.TransientModel):
    """
    检查通过
    """

    _name = "vehicle_maintain.inspect.confirm"
    _description = "Confirm the selected inspect"

    @api.multi
    def inspect_confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['maintain.manage.repair'].browse(active_ids):
            if record.state not in ('inspect'):
                raise UserError(_("Selected inspect(s) cannot be confirmed as they are not in 'inspect' state."))
            record.action_completed()
        return {'type': 'ir.actions.act_window_close'}



class MaintainInspectReturn(models.TransientModel):
    """
    退工返回
    """
    _name = "maintain.manage.inspect.return"
    _description = "Confirm return"

    return_reason = fields.Text("Return Reason", help="Return Reason")

    @api.multi
    def inspect_return(self):
        context = dict(self._context or {})
        active_id = context.get('active_id', '') or ''
        record = self.env['maintain.manage.repair'].browse(active_id)
        if record.state not in ('inspect',):
            raise UserError(_("Selected inspect(s) cannot be confirmed as they are not in 'inspect' state."))
        record.action_return(self.return_reason)
        return {'type': 'ir.actions.act_window_close'}
