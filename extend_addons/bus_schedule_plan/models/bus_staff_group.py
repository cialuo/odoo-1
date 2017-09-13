# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime
from datetime import timedelta
from bus_work_rule import BusWorkRules


class BusStaffGroup(models.Model):
    """
    人车配班
    """
    # _sql_constraints = [
    #     ('record_unique', 'unique(name)', _('The staff name must be unique!'))
    # ]
    _name = 'bus_staff_group'
    name = fields.Char("Staff Group Name", default="/")
    route_id = fields.Many2one('route_manage.route_manage', required=True)
    line_name = fields.Char(related="route_id.line_name")

    vehicle_line_ids = fields.One2many('bus_staff_group_vehicle_line', 'staff_group_id')

    vehicle_ct = fields.Integer(compute="_get_vehicle_ct")
    staff_date = fields.Date("Last Staff Date", default=fields.Date.today)

    move_time_id = fields.Many2one("scheduleplan.busmovetime")

    @api.multi
    def action_excute_records(self):
        BusWorkRules.genExcuteRecords(self.move_time_id)

    @api.depends("vehicle_line_ids")
    def _get_vehicle_ct(self):
        for i in self:
            i.vehicle_ct = len(i.vehicle_line_ids)

    @api.multi
    def action_gen_staff_group(self, route_id, move_time_id=None, staff_date=datetime.date.today(), operation_ct=0, force=False):
        """
        生成人车配班
        :param route_id: 线路
        :param move_time_id: 行车时间表
        :param staff_date: 行车时间
        :param operation_ct: 运营车辆数
        :param force: 是否强制更新班组信息
        :return:
        """
        use_date = datetime.datetime.strftime(staff_date-timedelta(days=1), "%Y-%m-%d")
        staff_date_str = datetime.datetime.strftime(staff_date, "%Y-%m-%d")

        res = self.env['bus_staff_group'].search([('name', '=', route_id.line_name + '/' + str(staff_date_str))])
        if res:
            res.unlink()

        if force:
            self.env['bus_group_driver_vehicle_shift'].scheduler_vehicle_shift(route_id.id, use_date=use_date)

        res_group_shift = self.env['bus_group_driver_vehicle_shift'].read_group(
                                        [('use_date', '=', staff_date_str), ('vehicle_sequence', '>', 0),
                                         ('route_id', '=', route_id.id)], ['vehicle_sequence'],
                                         groupby=['vehicle_sequence'], orderby='vehicle_sequence')

        if not res_group_shift:
            self.env['bus_group_driver_vehicle_shift'].scheduler_vehicle_shift(route_id.id, use_date=use_date)
            res_group_shift = self.env['bus_group_driver_vehicle_shift'].read_group(
                [('use_date', '=', staff_date_str), ('vehicle_sequence', '>', 0),
                 ('route_id', '=', route_id.id)], ['vehicle_sequence'],
                groupby=['vehicle_sequence'], orderby='vehicle_sequence')

        datas = []
        count = 0
        for j in res_group_shift:
            res_vehicles = self.env['bus_group_driver_vehicle_shift'].search(j['__domain'])
            sequence = 0
            data_shift = []
            for m in res_vehicles:
                sequence += 1
                vals_shift = {
                    'group_id': m.group_id.id,
                    "driver_id": m.driver_id.driver_id.id,
                    "conductor_id": m.conductor_id.conductor_id.id or None,
                    'bus_shift_id': m.bus_shift_id.id,
                    'bus_shift_choose_line_id': m.bus_shift_choose_line_id.id,
                    "sequence": sequence
                }
                data_shift.append((0, 0, vals_shift))
            if data_shift:
                count += 1
                vals = {
                    "route_id": res_vehicles[0].route_id.id,
                    'vehicle_id': res_vehicles[0].bus_group_vehicle_id.vehicle_id.id,
                    'operation_state': 'flexible',
                    'sequence': res_vehicles[0].vehicle_sequence,
                    'bus_group_id': res_vehicles[0].group_id.id,
                    'staff_line_ids': data_shift
                }
                if count <= operation_ct:
                    vals.update({'operation_state': 'operation'})
                datas.append((0, 0, vals))
        if not datas:
            raise exceptions.UserError(_('bus_group_driver_vehicle_shift is not exists,please check bus_group.'))
        return self.env['bus_staff_group'].create({'vehicle_line_ids': datas,
                                                   'route_id': route_id.id,
                                                   'move_time_id':move_time_id.id or None,
                                                   'name': route_id.line_name + '/' + staff_date_str,
                                                   'staff_date': staff_date
                                                  })



    # @api.onchange('route_id', 'bus_shift_id')
    # def _get_route_id_onchange(self):
    #     for i in self:
    #         datas = []
    #         for j in i.route_id.vehicle_res.ids:  #更新车辆  暂时不判断运营状态
    #             vals = {
    #                 "route_id": i.route_id.id,
    #                 'vehicle_id': j,
    #                 'operation_state': 'operation',
    #                 'bus_shift_id': i.bus_shift_id.id,
    #             }
    #             res = self.env['bus_group_vehicle'].search([('vehicle_id', '=', j)])
    #             if res:
    #                 bus_group_id = res[0].bus_group_id
    #                 vals.update({'bus_group_id':bus_group_id})
    #
    #             datas.append((0, 0, vals))
    #         i.vehicle_line_ids = datas


class BusStaffGroupVehicleLine(models.Model):
    """
    人车配班 车辆列表
    """
    _name = 'bus_staff_group_vehicle_line'
    _rec_name = 'vehicle_id'
    sequence = fields.Integer("Sequence")

    staff_group_id = fields.Many2one('bus_staff_group', readonly=True, ondelete='cascade')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True, readonly=True)
    state = fields.Selection(related='vehicle_id.state', readonly=True, string="Vehicle State")

    operation_state = fields.Selection([('operation', "operation"),
                                        ('flexible', "flexible")], default='operation', required=True)

    bus_group_id = fields.Many2one('bus_group', readonly=True)
    # is_conductor = fields.Boolean(related='bus_group_id.is_conductor')

    bus_group_driver_id = fields.Many2one("bus_group_driver", domain="[('bus_group_id','=',bus_group_id)]")
    bus_group_conductor_id = fields.Many2one("bus_group_conductor", domain="[('bus_group_id','=',bus_group_id)]")

    bus_shift_id = fields.Many2one('bus_shift', related='bus_group_id.bus_shift_id', readonly=True)
    bus_shift_choose_line_id = fields.Many2one('bus_shift_choose_line', domain="[('shift_id','=',bus_shift_id)]")

    staff_line_ids = fields.One2many('bus_staff_group_vehicle_staff_line', 'vehicle_line_id')

    staff_driver_names = fields.Char(string='Staff Driver Names', compute='_get_staff_names')

    staff_conductor_names = fields.Char(string='Staff Conductor Names', compute='_get_staff_names')

    @api.depends("staff_line_ids")
    def _get_staff_names(self):
        """
            功能：获取司机和售票员名字
        """
        for i in self:
            staff_driver_names = set()
            staff_conductor_names = set()
            for j in i.staff_line_ids:
                if j.driver_id:
                    staff_driver_names.add(j.driver_id.name)
                if j.conductor_id:
                    staff_conductor_names.add(j.conductor_id.name)

            i.staff_driver_names = ",".join(list(staff_driver_names))
            i.staff_conductor_names = ",".join(list(staff_conductor_names))

    @api.multi
    def dispatch_staff_line(self):
        """
        派班
        """
        self.ensure_one()
        # if not self.user_id:
        #     raise exceptions.UserError(_(""))
        vals = {
            "driver_id": self.bus_group_driver_id.driver_id.id,
            "conductor_id": self.bus_group_conductor_id.conductor_id.id or None,
            'bus_shift_choose_line_id': self.bus_shift_choose_line_id.id,
            "sequence": len(self.staff_line_ids)+1
        }
        self.write({
            'staff_line_ids': [(0, 0, vals)]
        })


class BusStaffGroupVehicleStaffLine(models.Model):
    """
    人车配班 车辆的司机和乘务员
    """
    _name = 'bus_staff_group_vehicle_staff_line'
    sequence = fields.Integer("Shift Line Sequence", default=1)
    vehicle_line_id = fields.Many2one('bus_staff_group_vehicle_line', ondelete='cascade')

    group_id = fields.Many2one('bus_group', 'Group')

    driver_id = fields.Many2one('hr.employee', string="driver", required=True,
                                domain="[('workpost.posttype', '=', 'driver')]")
    driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)

    conductor_id = fields.Many2one('hr.employee', string="conductor",
                                   domain="[('workpost.posttype', '=', 'conductor')]")
    conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)



    # driver_id = fields.Many2one("bus_group_driver", domain="[('bus_group_id','=',group_id)]")
    #
    # driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)
    #
    # conductor_id = fields.Many2one("bus_group_conductor", domain="[('bus_group_id','=',group_id)]")
    # conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)

    bus_shift_id = fields.Many2one('bus_shift', readonly=True)
    bus_shift_choose_line_id = fields.Many2one('bus_shift_choose_line', domain="[('shift_id','=',bus_shift_id)]")




