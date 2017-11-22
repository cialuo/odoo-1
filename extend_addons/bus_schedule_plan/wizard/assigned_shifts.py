# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from itertools import izip_longest
import datetime
from datetime import timedelta


class AssignedShifts(models.TransientModel):
    _name = 'assigned_shifts'

    group_id = fields.Many2one('bus_group', 'Group', ondelete='cascade', required=True)
    route_id = fields.Many2one('route_manage.route_manage', related='group_id.route_id', required=True)

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
        use_date = datetime.datetime.strptime(str(self.use_date), '%Y-%m-%d')

        yesterday = datetime.datetime.strptime(str(datetime.date.today()-timedelta(days=1)), '%Y-%m-%d')
        if len(self.bus_shift_id.shift_line_ids.ids)<1:
            raise UserError(_("The shift line is not exists， please choose the right shifts"))

        if use_date < yesterday:
            raise UserError(_("use_date is more than yesterday"))

        for i in self.driver_vehicle_shift_ids:
            i.unlink()

        driver_list = self.driver_ids.ids
        conductor_list = self.conductor_ids.ids
        if len(driver_list) < len(conductor_list): #售票员比司机多的情况
            raise UserError(_("The conductor is more than the driver"))

        vehicle_list = []
        for i in range(len(self.vehicle_ids.ids)):
            vehicle_list += [self.vehicle_ids.ids[i]] * len(self.bus_shift_id.shift_line_ids.ids)

        res = self.env['bus_group_driver_vehicle_shift'].search([('use_date', '=', self.use_date),
                                                                 ('route_id', '=', self.route_id.id),
                                                                 ('group_id', '!=', self.group_id.id)],
                                                                order='vehicle_sequence desc', limit=1)
        vehicle_sequence = 0
        if res:
            vehicle_sequence = res[0].vehicle_sequence

        vehicle_list = []
        t_sequence_list = []
        for i in range(len(self.vehicle_ids.ids)):
            vehicle_list += [self.vehicle_ids.ids[i]] * len(self.bus_shift_id.shift_line_ids.ids)
            t_sequence_list += [i+1+vehicle_sequence] * len(self.bus_shift_id.shift_line_ids.ids)

        shift_line_lists = self.bus_shift_id.shift_line_ids.ids * len(self.vehicle_ids.ids)

        xyz = izip_longest(driver_list, conductor_list, vehicle_list, shift_line_lists, t_sequence_list)
        datas = []
        sequence = 0
        for j in xyz:
            sequence = sequence +1 
            if self.group_id.is_flexible :
                vehicle_sequence = 0
            else:
                vehicle_sequence =  j[4]
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
                             'bus_shift_choose_line_id': j[3],
                             'vehicle_sequence': vehicle_sequence})
            datas.append((0, 0, data))
        self.write({'driver_vehicle_shift_ids': datas})
        return {
            'name': _('assigned_shifts'),
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
            flag = False
            driver_ids = []
            conductor_ids = []
            for j in wizard.driver_vehicle_shift_ids:
                if j.driver_id:
                    driver_ids.append(j.driver_id.id)
                if j.conductor_id:
                    conductor_ids.append(j.conductor_id.id)
            if len(driver_ids) > len(list(set(driver_ids))):#判断司机是否有重复
                raise UserError(_("There are duplicate driver"))
            if len(conductor_ids)>len(list(set(conductor_ids))):#判断售票员是否有重复
                raise UserError(_("There are duplicate conductor"))

            #删除之前的初始化数据
            self.env['bus_group_driver_vehicle_shift'].search([('use_date', '=', self.use_date),
                                                               ('group_id', '=', self.group_id.id)]).unlink()

            for j in wizard.driver_vehicle_shift_ids:
                data = {
                    'sequence': j.sequence,
                    'use_date': j.use_date,
                    'group_id': j.group_id.id,
                    'driver_id': j.driver_id.id,
                    'conductor_id': j.conductor_id.id,
                    'vehicle_sequence': j.vehicle_sequence,
                    'bus_shift_id': j.bus_shift_id.id,
                    'bus_shift_choose_line_id': j.bus_shift_choose_line_id.id,
                    'bus_group_vehicle_id': j.bus_group_vehicle_id.id
                }
                self.env['bus_group_driver_vehicle_shift'].create(data)
                flag = True
            if flag and self.group_id.state == 'use':
                self.group_id.write({'state': 'wait_check'})
        return False


class BusGroupDriverVehicleShiftTran(models.TransientModel):
    _name = 'bus_group_driver_vehicle_shift_tran'

    assign_id = fields.Many2one('assigned_shifts', ondelete='cascade', readonly=True)

    sequence = fields.Integer("Shift Line Sequence", default=1, readonly=False)

    group_id = fields.Many2one('bus_group', 'Group', ondelete='cascade', required=True)
    route_id = fields.Many2one('route_manage.route_manage', related='group_id.route_id', required=True)
    bus_shift_id = fields.Many2one('bus_shift', readonly=True)
    bus_shift_choose_line_id = fields.Many2one('bus_shift_choose_line', domain="[('shift_id','=',bus_shift_id)]")

    choose_sequence = fields.Integer(related='bus_shift_choose_line_id.sequence')

    driver_id = fields.Many2one("bus_group_driver", domain="[('bus_group_id','=',group_id)]")
    driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)

    conductor_id = fields.Many2one("bus_group_conductor", domain="[('bus_group_id','=',group_id)]")
    conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)

    bus_group_vehicle_id = fields.Many2one("bus_group_vehicle", domain="[('bus_group_id','=',group_id)]")
    vehicle_sequence = fields.Integer("Vehicle Sequence", readonly=False)

    use_date = fields.Date(default=fields.Date.context_today, readonly=True)
