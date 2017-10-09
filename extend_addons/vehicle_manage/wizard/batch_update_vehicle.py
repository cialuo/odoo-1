# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import datetime


class BatchUpdateVehicle(models.TransientModel):
    _name = 'batch_update_vehicle'

    # 状态（车辆生命周期）
    WORKFLOW_STATE_SELECTION = [
        ('invest_period', 'Invest period'),
        ('operation_period', 'Operation period'),
    ]

    vehicle_tran_ids = fields.One2many('batch_update_vehicle_tran', 'batch_id')

    vehicle_life_state = fields.Selection(WORKFLOW_STATE_SELECTION,
                                          default='invest_period',
                                          string='Vehicle life cycle state', required=True)

    @api.multi
    def import_vehicle(self):
        self.vehicle_tran_ids.unlink()
        res = self.env['fleet.vehicle'].search([('vehicle_life_state', '=', self.vehicle_life_state),
                                                ('entry_state', '=', 'audited')])
        datas = []
        for j in res:
            data = {
                'vehicle_id': j.id,
            }
            datas.append((0, 0, data))
        self.write({'vehicle_tran_ids': datas})

        return {
            'name': _('batch_update_vehicle'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'batch_update_vehicle',
            'res_id': self.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def action_batch_update_vehicle(self):
        if self.vehicle_life_state == 'operation_period':
            for i in self.vehicle_tran_ids:
                i.vehicle_id.vehicle_life_state = 'scrap_period'
                i.vehicle_id.forced_destroy_date = datetime.date.today()
            return False
        else:
            not_match_list = []
            match_list = []
            for j in self.vehicle_tran_ids:
                if not j.vehicle_id.investment_ids:
                    #2017-9-19 提出 不配置费用也可以投入运营
                    match_list.append(j)
                    # not_match_list.append(j)
                    continue
                flag = False
                for k in j.vehicle_id.investment_ids:
                    if k.is_required == 'yes':
                        if k.cost_amount <= 0:
                            not_match_list.append(j)
                            flag = False
                            break
                    flag = True
                if flag:
                    match_list.append(j)
            if match_list:
                for i in match_list:
                    vals = {"vehicle_life_state": 'operation_period',
                            "start_service_date": datetime.date.today()
                            }

                    vehicle_code = i.vehicle_id.vehicle_code + datetime.date.today().strftime('%Y')[-2:]
                    vals.update({"vehicle_code":vehicle_code})
                    i.vehicle_id.write(vals)
            if not_match_list:
                datas = []
                for j in not_match_list:
                    datas.append(j.id)
                self.write({'vehicle_tran_ids': [(6, 0, datas)]})

                return {
                    'name': _('batch_update_vehicle_warning'),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'batch_update_vehicle',
                    'res_id': self.id,
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                    'view_id': self.env.ref('vehicle_manage.view_batch_update_vehicle_status_warn').id
                }


class BatchUpdateVehicleTran(models.TransientModel):
    _name = 'batch_update_vehicle_tran'

    batch_id = fields.Many2one('batch_update_vehicle', ondelete='cascade', readonly=True)

    vehicle_id = fields.Many2one('fleet.vehicle', string='vehicle', readonly=True)
    license_plate = fields.Char(required=True, related='vehicle_id.license_plate', readonly=True)

    vehicle_life_state = fields.Selection(related='vehicle_id.vehicle_life_state',
                                          string='Vehicle life cycle state',
                                          readonly=True)




