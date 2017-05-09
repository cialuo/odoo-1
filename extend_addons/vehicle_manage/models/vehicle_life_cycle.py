# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# 车辆生命周期
class vehicle_life(models.Model):
    # 表名
    _inherit = "fleet.vehicle"

    @api.multi
    def _add_default_value(self):
        print('-------------------')
        res = self.env['cost_type_set.cost_type_set'].search([('state', '=', 'inuse')])
        datas = []
        for i in res:
            print ("=======%s" % i.type_name)
            data = {
                'is_required': i.is_required,
                'cost_type': i.type_name,
            }
            datas.append((0, 0, data))
        return datas

    investment_ids = fields.One2many('investment_cost', 'vehicle_id', string='Investments', default=_add_default_value)

    WORKFLOW_STATE_SELECTION = [
        ('invest_period', _('Invest period')),
        ('operation_period', _('Operation period')),
        ('scrap_period', _('Scrap period'))
    ]

    vehicle_life_state = fields.Selection(WORKFLOW_STATE_SELECTION,
                                          default='invest_period',
                                          string=_('Vehicle life cycle state'),
                                          readonly=True)

    @api.multi
    def action_operation(self):
        print('operation_period')
        self.vehicle_life_state = 'operation_period'
        return True

    @api.multi
    def action_scrap(self):
        print('scrap_period')
        self.vehicle_life_state = 'scrap_period'
        return True

# 投入期费用
class investment_period_cost(models.Model):
    _name = 'investment_cost'

    _rec_name = 'cost_name'
    cost_amount = fields.Integer(_('Cost amount'))
    cost_name = fields.Char(_('Cost name'))
    occurrence_time = fields.Datetime(_('Occurrence time'))
    cost_type = fields.Char(_('Cost type'))
    is_required = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='yes', string=_('Is_required'))
    total_amount = fields.Integer(_('Total amount'))

    WORKFLOW_STATE_SELECTION = [
        ('inuse', _('In-use')),
        ('archive', _('Archive'))
    ]
    vehicle_id = fields.Many2one('fleet.vehicle', string='Investment id')



