# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import datetime


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
    lineName = fields.Char(related="route_id.lineName")
    # bus_algorithm_id = fields.Many2one('bus_algorithm', required=True)
    # bus_algorithm_date = fields.Date()
    # bus_driver_algorithm_id = fields.Many2one('bus_driver_algorithm', required=True)
    # bus_driver_algorithm_date = fields.Date()

    # bus_shift_id = fields.Many2one('bus_shift', required=True)

    vehicle_line_ids = fields.One2many('bus_staff_group_vehicle_line', 'staff_group_id')

    vehicle_ct = fields.Integer(compute="_get_vehicle_ct")


    @api.model
    def create(self, data):
        """
        报修单:
            功能：自动生成人车配班名称 线路名称/当前日期
        """
        if data.get('name', '/') == '/':
            data['name'] = data['lineName'] + '/' + str(datetime.date.today())
        res = super(BusStaffGroup, self).create(data)
        return res

    # @api.onchange('bus_algorithm_id')
    # def _get_algorithm_date_onchange(self):
    #     for i in self:
    #         if i.bus_algorithm_id:
    #             i.bus_algorithm_date = datetime.date.today()
    #
    # @api.onchange('bus_driver_algorithm_id')
    # def _get_driver_algorithm_date_onchange(self):
    #     for i in self:
    #         if i.bus_driver_algorithm_id:
    #             i.bus_driver_algorithm_date = datetime.date.today()

    @api.depends("vehicle_line_ids")
    def _get_vehicle_ct(self):
        for i in self:
            i.vehicle_ct = len(i.vehicle_line_ids)


    @api.onchange('route_id')
    def _get_route_id_onchange(self):
        for i in self:
            datas = []
            k = 2
            res = self.env['bus_group_vehicle'].search([('route_id', '=', i.route_id.id)])
            for j in res:  #更新车辆  暂时不判断运营状态
                vals = {
                    "route_id": i.route_id.id,
                    'vehicle_id': j.vehicle_id.id,
                    'operation_state': 'flexible',
                    'sequence': j.sequence,
                    'bus_group_id': j.bus_group_id
                }
                if j.sequence <= k:
                    vals.update({'operation_state': 'operation'})

                datas.append((0, 0, vals))
            i.vehicle_line_ids = datas


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

    @api.model
    def scheduler_manage_auto_staff_group(self):
        staff_groups = self.read_group([], ['route_id'], groupby=['route_id'])
        for i in staff_groups:
            res = self.search(i['__domain'], order='id desc', limit=1)
            print res
            d2 = datetime.datetime.strptime(res.bus_driver_algorithm_date, '%Y-%m-%d')
            d1 = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
            print d1 ,d2  ,res.bus_driver_algorithm_id.cycle
            if (d1-d2).days < res.bus_driver_algorithm_id.cycle: #未达到周期数
                bus_algorithm_driver_date = res.bus_algorithm_date
            else:
                bus_algorithm_driver_date = datetime.date.today()

            vals = {
                'name': res.lineName + '/' + str(datetime.date.today()),
                'route_id': res.route_id.id,
                'bus_algorithm_id': res.bus_algorithm_id.id,
                'bus_driver_algorithm_id': res.bus_driver_algorithm_id.id,
                'bus_algorithm_driver_date': bus_algorithm_driver_date,
                'bus_shift_id': res.bus_shift_id.id
            }
            print vals

    @api.model
    def run_scheduler(self):
        self.scheduler_manage_auto_staff_group()


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
    is_conductor = fields.Boolean(related='bus_group_id.is_conductor')

    bus_group_driver_id = fields.Many2one("bus_group_driver", domain="[('bus_group_id','=',bus_group_id)]")
    bus_group_conductor_id = fields.Many2one("bus_group_conductor", domain="[('bus_group_id','=',bus_group_id)]")

    bus_shift_id = fields.Many2one('bus_shift', related='bus_group_id.bus_shift_id', readonly=True)
    bus_shift_line_id = fields.Many2one('bus_shift_line', domain="[('shift_id','=',bus_shift_id)]")

    staff_line_ids = fields.One2many('bus_staff_group_vehicle_staff_line', 'vehicle_line_id')
    staff_names = fields.Char(string='Staff Names', compute='_get_staff_names')

    @api.depends("staff_line_ids")
    def _get_staff_names(self):
        """
        司机:
            功能：获取司机名字
        """
        for i in self:
            staff_names = set()
            for j in i.staff_line_ids:
                staff_names.add(j.driver_id.name)
            i.staff_names = ",".join(list(staff_names))



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
            'bus_shift_line_id': self.bus_shift_line_id.id,
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
    driver_id = fields.Many2one('hr.employee', string="driver", required=True,
                                domain="[('workpost.posttype', '=', 'driver')]")
    driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)

    conductor_id = fields.Many2one('hr.employee', string="conductor",
                                   domain="[('workpost.posttype', '=', 'conductor')]")
    conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)

    bus_shift_line_id = fields.Many2one('bus_shift_line')



