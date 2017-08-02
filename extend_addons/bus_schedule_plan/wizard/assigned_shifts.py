# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AssignedShifts(models.TransientModel):
    _name = 'assigned_shifts'

    group_id = fields.Many2one('bus_group', 'Group', required=True)

    driver_vehicle_shift_ids = fields.One2many('bus_group_driver_vehicle_shift_tran', 'assign_id')

    driver_ids = fields.One2many('bus_group_driver', 'bus_group_id',
                                 related='group_id.driver_ids')

    conductor_ids = fields.One2many('bus_group_conductor', 'bus_group_id',
                                    related='group_id.conductor_ids')

    bus_shift_id = fields.Many2one('bus_shift', related='group_id.bus_shift_id', readonly=True)
    vehicle_ids = fields.One2many('bus_group_vehicle', 'bus_group_id', related='group_id.vehicle_ids')

    use_date = fields.Date(default=fields.Date.context_today)

    @api.model
    def default_get(self, fields):
        res = super(AssignedShifts, self).default_get(fields)
        if self.env.context.get('active_id') and self.env.context.get('active_model') == 'bus_group':
            s_group = self.env['bus_group'].browse(self.env.context['active_id'])
        if 'group_id' in fields and not res.get('group_id') and s_group:
            res['group_id'] = s_group.id
        return res

    @api.multi
    def import_driver(self):

        driver_list = self.driver_ids.ids
        conductor_list = self.conductor_ids.ids
        if len(driver_list) < len(conductor_list): #售票员比司机多的情况
            pass
        vehicle_list = []

        for i in range(len(self.vehicle_ids.ids)):
            vehicle_list += [self.vehicle_ids.ids[i]] * len(self.bus_shift_id.shift_line_ids.ids)

        shift_line_lists = self.bus_shift_id.shift_line_ids.ids * len(self.vehicle_ids.ids)
        vehicle_list = vehicle_list + ['']*(len(driver_list)-len(vehicle_list))
        shift_line_lists = shift_line_lists + [''] * (len(driver_list) - len(shift_line_lists))

        for i in self.driver_vehicle_shift_ids:
            i.unlink()
        sequence = 0
        xyz = zip(driver_list, conductor_list, vehicle_list,shift_line_lists)
        datas = []
        for j in xyz:
            print j
            sequence += 1
            data = {
                'sequence': sequence,
                'driver_id': j[0],
                'conductor_id': j[1],
                'group_id': self.group_id.id,
                'use_date': self.use_date,
                'bus_shift_id': self.bus_shift_id.id
            }
            if j[2]:
                data.update({'bus_group_vehicle_id': j[2],
                             'bus_shift_choose_line_id': j[3]})
            datas.append((0, 0, data))
        self.write({'driver_vehicle_shift_ids': datas})
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'assigned_shifts',
            'res_id': self.id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_active_id': self._context.get('active_id')}
        }

    @api.multi
    def assigned_shifts(self):
        for wizard in self:
            print wizard.driver_vehicle_shift_ids
        return False


class BusGroupDriverVehicleShiftTran(models.TransientModel):
    _name = 'bus_group_driver_vehicle_shift_tran'

    assign_id = fields.Many2one('assigned_shifts', ondelete='cascade', readonly=True)

    sequence = fields.Integer("Shift Line Sequence", default=1, readonly=True)

    group_id = fields.Many2one('bus_group', 'Group', required=True)
    bus_shift_id = fields.Many2one('bus_shift', readonly=True)
    bus_shift_choose_line_id = fields.Many2one('bus_shift_choose_line', domain="[('shift_id','=',bus_shift_id)]")

    driver_id = fields.Many2one("bus_group_driver", domain="[('bus_group_id','=',group_id)]")
    driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)

    conductor_id = fields.Many2one("bus_group_conductor", domain="[('bus_group_id','=',group_id)]")
    conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)

    bus_group_vehicle_id = fields.Many2one("bus_group_vehicle", domain="[('bus_group_id','=',group_id)]")
    t_sequence = fields.Integer("T Sequence", related='bus_group_vehicle_id.sequence', readonly=True)

    use_date = fields.Date(default=fields.Date.context_today, readonly=True)
