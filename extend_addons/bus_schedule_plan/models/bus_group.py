# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime


class BusGroup(models.Model):
    """
    班组管理
    """
    _name = 'bus_group'

    _sql_constraints = [
        ('record_unique', 'unique(route_id,name)', _('The route and name must be unique!'))
    ]

    name = fields.Char('Group Name', required=True)
    route_id = fields.Many2one('route_manage.route_manage', required=True)
    # is_conductor = fields.Boolean(default=True)

    vehicle_ct = fields.Integer(compute='get_vehicle_ct')
    driver_ct = fields.Integer(compute='get_driver_ct')
    conductor_ct = fields.Integer(compute='get_conductor_ct')

    vehicle_ids = fields.One2many('bus_group_vehicle', 'bus_group_id')
    driver_ids = fields.One2many('bus_group_driver', 'bus_group_id')
    conductor_ids = fields.One2many('bus_group_conductor', 'bus_group_id')

    bus_algorithm_id = fields.Many2one('bus_algorithm', required=True)
    is_algorithm_change = fields.Boolean(default=False)
    bus_algorithm_date = fields.Date(default=fields.Date.context_today)
    bus_driver_algorithm_id = fields.Many2one('bus_driver_algorithm', required=True)
    bus_driver_algorithm_date = fields.Date(default=fields.Date.context_today)
    is_driver_algorithm_change = fields.Boolean(default=False)

    bus_shift_id = fields.Many2one('bus_shift', required=True)

    driver_vehicle_shift_ids = fields.One2many('bus_group_driver_vehicle_shift', 'group_id')

    is_not_match = fields.Boolean(default=False, compute='check_vehicle_is_match')
    not_match_reason = fields.Text(compute='check_vehicle_is_match')

    state = fields.Selection([
        ('draft', 'draft'),
        ('wait_check', "wait_check"),
        ('use', "use"),], string='Bus Group State', default='draft', readonly=True)



    @api.multi
    def action_test(self):
        """
        1.大轮换
        2.车辆轮趟算法
        3.轮班算法

        """

        res = self.env['bus_group_driver_vehicle_shift'].search([('route_id','=',self.route_id.id),
                                                                 ('use_date','=','2017-08-05')])

        for i in res:
            i.unlink()

        res_se = self.env['bus_group_driver_vehicle_shift'].read_group(
            [('use_date', '=', '2017-08-04'),
             ('route_id', '=', self.route_id.id)],
            ['t_sequence'], ['t_sequence']) #查出所有的组
        old_list = []
        for i in res_se:
            if i['t_sequence'] == 0:
                continue
            old_list.append(i['t_sequence'])
        new_list = sorted(old_list, reverse=True)

        res_group_shift = self.env['bus_group_driver_vehicle_shift'].read_group(
            [('use_date', '=', '2017-08-04'),
             ('route_id', '=', self.route_id.id)],
            ['group_id'],
            groupby=['group_id'])

        old_group_dict = {}
        new_group_dict = {}
        for j in res_group_shift:
            # if not j['bus_group_vehicle_id']:
            #     continue
            res_vehicles = self.env['bus_group_driver_vehicle_shift'].search(j['__domain'])

            group_seq = []
            for i in res_vehicles:
                if i.t_sequence == 0:
                    continue
                group_seq.append(i.t_sequence)
            old_group_dict[j['group_id'][0]] = list(set(group_seq))
            new_group_dict[j['group_id'][0]] = []
        # print old_group_dict
        # print new_group_dict


        """   大轮换 start   """

        is_big = True
        if is_big:
            xyz = zip(old_list, new_list)
            datas = []
            # for j in xyz:
            for k, v in old_group_dict.iteritems():
                tmp = []
                for m in v:
                    tmp.append(new_list[old_list.index(m)])
                new_group_dict[k] = tmp

        """   大轮换 end   """



        """   车辆轮班算法 start  """

        new_group_dict_driver = {}
        for k, v in new_group_dict.iteritems():

            s_res = self.env['bus_group'].search([('id','=',k)])
            cycle = s_res[0].bus_driver_algorithm_id.cycle
            direction = s_res[0].bus_driver_algorithm_id.direction

            bus_driver_algorithm_date = s_res[0].bus_driver_algorithm_date
            bus_driver_algorithm_date = datetime.datetime.strptime(bus_driver_algorithm_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
            if cycle > 0:
                if (end_date - bus_driver_algorithm_date).days >= cycle:

                    def leftMove2(list, step):
                        l = list[:step]
                        for m in range(step, len(list)):
                            list[m - step] = list[m]
                        list[len(list) - step:] = l
                        return list

                    if direction == 'positive': #negative
                        b = v.pop()
                        v.insert(0, b)
                    else:
                        v = leftMove2(v, 1)
            new_group_dict_driver[k] = v

        for k, v in new_group_dict.iteritems():
            s_res = self.env['bus_group'].search([('id','=',k)])
            cycle = s_res[0].bus_algorithm_id.cycle
            direction = s_res[0].bus_algorithm_id.direction
            bus_algorithm_date = s_res[0].bus_driver_algorithm_date

            bus_algorithm_date = datetime.datetime.strptime(bus_algorithm_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")

            res_group_s = self.env['bus_group_driver_vehicle_shift'].search(
                [('route_id', '=', self.route_id.id),
                 ('use_date', '=', '2017-08-04'),
                 ('group_id', '=', k)])

            shift_list = res_group_s.mapped('choose_sequence')

            old_shift_list = shift_list[:]

            if cycle > 0:
                if (end_date - bus_algorithm_date).days >= cycle:
                    def leftMove2(list, step):
                        l = list[:step]
                        for m in range(step, len(list)):
                            list[m - step] = list[m]
                        list[len(list) - step:] = l
                        return list

                    if direction == 'positive': #negative
                        b = shift_list.pop()
                        shift_list.insert(0, b)
                    else:
                        shift_list = leftMove2(shift_list, 1)

            res_group_shift_yest = self.env['bus_group_driver_vehicle_shift'].search(
                            [('use_date', '=', '2017-08-04'),
                             ('route_id', '=', self.route_id.id),
                             ('group_id', '=', k)
                 ])

            count = 0
            for j in res_group_shift_yest:
                new_choose_sequence = shift_list[count]
                bus_shift_choose_line_id = None
                if new_choose_sequence>0:
                    bus_shift_choose_line = s_res[0].bus_shift_id.shift_line_ids.filtered(lambda x: x.sequence == new_choose_sequence)
                    bus_shift_choose_line_id = bus_shift_choose_line.id

                data = {
                    'sequence': j.sequence,
                    'use_date': '2017-08-05',
                    'group_id': j.group_id.id,
                    'driver_id': j.driver_id.id,
                    'conductor_id': j.conductor_id.id,

                    # 't_sequence': new_t_sequence ,
                    # 'bus_group_vehicle_id': j.bus_group_vehicle_id.id,

                    'bus_shift_id': j.bus_shift_id.id,
                    'bus_shift_choose_line_id': bus_shift_choose_line_id or None,

                }
                self.env['bus_group_driver_vehicle_shift'].create(data)
                count += 1
            res_group_shift_today = self.env['bus_group_driver_vehicle_shift'].search(
                [('use_date', '=', '2017-08-05'),
                 ('route_id', '=', self.route_id.id),
                 ('group_id', '=', k)
                 ])
            for i in res_group_shift_today.mapped('bus_shift_choose_line_id').ids:

                res_group_shift_today_s = self.env['bus_group_driver_vehicle_shift'].search(
                    [('use_date', '=', '2017-08-05'),
                     ('route_id', '=', self.route_id.id),
                     ('group_id', '=', k),
                     ('bus_shift_choose_line_id', '=', i),
                     ])

                for m in zip(res_group_shift_today_s,old_group_dict[k]):
                    new_t_sequence = new_group_dict_driver[k][old_group_dict[k].index(m[1])]
                    data = {
                        't_sequence': new_t_sequence ,
                        'bus_group_vehicle_id': res_group_s.filtered(lambda x: x.t_sequence == m[1])[0].bus_group_vehicle_id.id
                        }
                    m[0].write(data)




    @api.multi
    def write(self, vals):
        if "bus_algorithm_id" in vals or 'bus_driver_algorithm_id' in vals or 'bus_shift_id' in vals or 'driver_vehicle_shift_ids' in vals:
            vals.update({'state': 'wait_check'})
        if "bus_algorithm_id" in vals:
            vals.update({'is_algorithm_change': True})
        if "bus_driver_algorithm_id" in vals:
            vals.update({'is_driver_algorithm_change': True})
        return super(BusGroup, self).write(vals)

    @api.multi
    def action_submit(self):
        """
        提交审核
        """
        self.write({
            'state': 'wait_check'
        })

    @api.multi
    def action_check(self):
        """
        审核通过
        """
        vals = {'state': 'use'}
        if self.is_algorithm_change:
            vals.update({'bus_algorithm_date':datetime.date.today()})
        if self.is_driver_algorithm_change:
            vals.update({'bus_driver_algorithm_date': datetime.date.today()})
        self.write(vals)

    @api.depends('vehicle_ids', 'driver_ids', 'bus_shift_id')
    def check_vehicle_is_match(self):
        for i in self:
            vehicle_ct = len(i.vehicle_ids)
            driver_ct = len(i.driver_ids)
            shift_ct = len(i.bus_shift_id.shift_line_ids)
            if vehicle_ct and shift_ct and driver_ct:
                if vehicle_ct * shift_ct > driver_ct:
                    i.is_not_match = True
                    i.not_match_reason = u'所选的班制，车辆数，司机数配置不合理，建议重新选择'

    @api.depends('vehicle_ids')
    def get_vehicle_ct(self):
        for i in self:
            i.vehicle_ct = len(i.vehicle_ids)

    @api.depends('driver_ids')
    def get_driver_ct(self):
        for i in self:
            i.driver_ct = len(i.driver_ids)

    @api.depends('conductor_ids')
    def get_conductor_ct(self):
        for i in self:
            i.conductor_ct = len(i.conductor_ids)

    @api.onchange('route_id')
    def _get_route_id_onchange(self):
        for i in self:
            datas = []
            count = 0
            res = self.env['bus_group'].search([('route_id', '=', i.route_id.id)])
            vehicle_lists = []
            driver_lists = []
            conductor_lists = []

            for k in res:
                if k.name == self.name:
                    continue
                vehicle_lists = vehicle_lists + k.vehicle_ids.mapped('vehicle_id').ids
                driver_lists = driver_lists + k.driver_ids.mapped('driver_id').ids
                conductor_lists += k.conductor_ids.mapped('conductor_id').ids
            for j in i.route_id.vehicle_res.ids:  #更新车辆
                if j in vehicle_lists:
                    continue
                vals = {
                    # 'sequence': count+len(lists),
                    "route_id": i.route_id.id,
                    'vehicle_id': j,
                }
                datas.append((0, 0, vals))
            i.vehicle_ids = datas

            datas = []
            for j in i.route_id.human_resource.filtered(lambda field: field.workpost.posttype == "driver").ids: #更新司机
                if j in driver_lists:
                    continue
                vals = {
                    "route_id": i.route_id.id,
                    'driver_id': j,
                }
                datas.append((0, 0, vals))
            i.driver_ids = datas

            datas = []
            for j in i.route_id.human_resource.filtered(lambda field: field.workpost.posttype == "conductor").ids: #更新乘务员
                if j in conductor_lists:
                    continue
                vals = {
                    "route_id": i.route_id.id,
                    'conductor_id': j,
                }
                datas.append((0, 0, vals))
            i.conductor_ids = datas


class BusGroupVehicle(models.Model):
    """
    班组车辆
    """
    _name = 'bus_group_vehicle'
    _rec_name = 'vehicle_id'

    _sql_constraints = [
        ('record_unique', 'unique(route_id,vehicle_id)', _('The route and vehicle must be unique!')),
        # ('sequence_unique', 'unique(sequence,route_id)', _('The sequence must be unique!'))
    ]

    bus_group_id = fields.Many2one('bus_group', ondelete='cascade')
    sequence = fields.Integer("Station Sequence", default=0, readonly=True)
    route_id = fields.Many2one('route_manage.route_manage')
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle No", help='Vehicle No', required=True,
                                 domain="[('route_id','=',route_id)]")
    vehicle_type = fields.Many2one("fleet.vehicle.model", related='vehicle_id.model_id',
                                   readonly=True, copy=False)
    ride_number = fields.Integer('Ride Number', related='vehicle_id.ride_number', readonly=True)
    state = fields.Selection(related='vehicle_id.state', readonly=True, string="Vehicle State")

    # @api.model
    # def create(self, data):
    #     """
    #         功能：序号自增长
    #     """
    #     if data.get('sequence', 0) and 'route_id' in data:
    #         res = self.env['bus_group'].search([('route_id', '=', data['route_id'])])
    #         lists = []
    #         for k in res:
    #             lists += k.vehicle_ids.mapped('vehicle_id').ids
    #         data['sequence'] = len(lists) + 1
    #     print data['sequence']
    #     res = super(BusGroupVehicle, self).create(data)
    #     return res


class BusGroupDriver(models.Model):
    """
    班组司机
    """
    _name = 'bus_group_driver'
    _rec_name = 'driver_id'

    route_id = fields.Many2one('route_manage.route_manage', readonly=True)
    bus_group_id = fields.Many2one('bus_group', ondelete='cascade')

    driver_id = fields.Many2one('hr.employee', string="driver", required=True,
                                domain="[('workpost.posttype', '=', 'driver')]")
    jobnumber = fields.Char(string='employee work number', related='driver_id.jobnumber', readonly=True)


class BusGroupConductor(models.Model):
    """
    班组乘务员
    """
    _name = 'bus_group_conductor'
    _rec_name = 'conductor_id'

    bus_group_id = fields.Many2one('bus_group', ondelete='cascade')
    conductor_id = fields.Many2one('hr.employee', string="conductor", required=True,
                                   domain="[('workpost.posttype', '=', 'conductor')]")
    jobnumber = fields.Char(string='employee work number', related='conductor_id.jobnumber', readonly=True)


class BusGroupDriverVehicleShift(models.Model):
    _name = 'bus_group_driver_vehicle_shift'

    use_date = fields.Date(default=fields.Date.context_today, readonly=True)
    vehicle_line_id = fields.Many2one('bus_staff_group_vehicle_line', ondelete='cascade')

    group_id = fields.Many2one('bus_group', ondelete='cascade', readonly=True)
    route_id = fields.Many2one('route_manage.route_manage', related='group_id.route_id')
    sequence = fields.Integer("Shift Line Sequence", default=1, readonly=True)

    driver_id = fields.Many2one("bus_group_driver")
    driver_jobnumber = fields.Char(string='driver_jobnumber', related='driver_id.jobnumber', readonly=True)

    conductor_id = fields.Many2one("bus_group_conductor")
    conductor_jobnumber = fields.Char(string='conductor_jobnumber', related='conductor_id.jobnumber', readonly=True)

    bus_shift_id = fields.Many2one('bus_shift', readonly=True)
    bus_shift_choose_line_id = fields.Many2one('bus_shift_choose_line')

    choose_sequence = fields.Integer(related='bus_shift_choose_line_id.sequence')

    bus_group_vehicle_id = fields.Many2one("bus_group_vehicle")
    t_sequence = fields.Integer("T Sequence", readonly=True)
