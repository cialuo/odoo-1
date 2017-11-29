# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import re
import time
from utils import check_time_format


class BusShift(models.Model):
    """
     班制管理
    """
    _name = 'bus_shift'

    name = fields.Char('Bus Shift Name', required=True)
    shift_ct = fields.Integer(compute='_get_shift_ct')
    shift_line_ids = fields.One2many('bus_shift_choose_line', 'shift_id')

    @api.depends('shift_line_ids')
    def _get_shift_ct(self):
        for i in self:
            i.shift_ct = len(i.shift_line_ids)


class BusShiftChooseLine(models.Model):
    """
     班制 班制下的班次详情
    """
    _name = 'bus_shift_choose_line'
    _rec_name = 'shift_line_id'

    _sql_constraints = [
        ('record_unique', 'unique(shift_id,shift_line_id)', _('The record must be unique!')),
    ]

    shift_id = fields.Many2one('bus_shift', ondelete='cascade')
    sequence = fields.Integer("Shift Line Sequence", required=True)
    shift_line_id = fields.Many2one('bus_shift_line', string='Shift Name', required=True)

    @api.model
    def create(self, data):
        """
        功能：序号自增长
        """
        sequence = 0
        if data.get('sequence', 0) == 0 or data.get('sequence', 0):
            res = self.env['bus_shift_choose_line'].search([('shift_id', '=', data['shift_id'])],
                                                           limit=1, order='sequence DESC')
            if res:
                sequence = res[0].sequence
        data['sequence'] = sequence + 1
        res = super(BusShiftChooseLine, self).create(data)
        return res


class BusShiftLine(models.Model):
    """
     班次列表
    """
    _name = 'bus_shift_line'

    _sql_constraints = [
        ('name_unique', 'unique(name)', _('The name must be unique!'))
    ]

    name = fields.Char('Shift Line Name', required=True)
    detail_ids = fields.One2many('bus_shift_line_detail', 'shift_line_id')

    @api.constrains('detail_ids')
    def onchange_detail(self):

        for i in self:
            for j in i.detail_ids:
                if j.start_time:
                    if not check_time_format(j.start_time):
                        raise exceptions.ValidationError(_("Time format is not correct"))
                if j.end_time:
                    if not check_time_format(j.end_time):
                        raise exceptions.ValidationError(_("Time format is not correct"))

    def time_cmp(self, start_time, end_time):
        """
        比较开始时间和结束时间的大小
        :param start_time:
        :param end_time:
        :return:
        """
        start_time = time.strptime(start_time, "%H:%M")
        end_time = time.strptime(end_time, "%H:%M")
        return int(time.strftime("%H%M", start_time)) - int(time.strftime("%H%M", end_time))

    def is_repeat_time(self, start_time1, end_time1, start_time2, end_time2):
        """
        比较两个区间的时间是否有重复
        :param start_time1:
        :param end_time1:
        :param start_time2:
        :param end_time2:
        :return:
        """
        start_time1 = int(time.strftime("%H%M", time.strptime(start_time1, "%H:%M")))
        end_time1 = int(time.strftime("%H%M", time.strptime(end_time1, "%H:%M")))
        start_time2 = int(time.strftime("%H%M", time.strptime(start_time2, "%H:%M")))
        end_time2 = int(time.strftime("%H%M", time.strptime(end_time2, "%H:%M")))
        if (max(start_time1, start_time2) < min(end_time1, end_time2)):
            return True
        return False

    def check_detail_time(self, detail_ids):
        """
        1,判断开始时间是否大于和等于结束时间
        2，两两判断时间是否有重复
        判断时间是否有重复
        """
        for i in detail_ids:
            if self.time_cmp(i.start_time, i.end_time) >= 0:
                raise exceptions.ValidationError(_("start time must be less than end time"))

        if len(detail_ids) > 1:
            for i in range(len(detail_ids)):
                start_time1 = detail_ids[i].start_time
                end_time1 = detail_ids[i].end_time
                for j in range(i+1, len(detail_ids)):
                    start_time2 = detail_ids[j].start_time
                    end_time2 = detail_ids[j].end_time
                    if self.is_repeat_time(start_time1, end_time1, start_time2, end_time2):
                        raise exceptions.ValidationError(_("Time has repeated"))

    @api.model
    def create(self, data):
        """
        新增时判断时间是否有重复
        """
        res = super(BusShiftLine, self).create(data)
        detail_ids = data['detail_ids']
        if detail_ids and self.detail_ids:
            self.check_detail_time(self.detail_ids)
        return res

    @api.multi
    def write(self, vals):
        """
        修改时判断时间是否有重复
        """
        res = super(BusShiftLine, self).write(vals)
        if 'detail_ids' in vals and vals.get('detail_ids', ''):
            self.check_detail_time(self.detail_ids)
        return res


class BusShiftLineDetail(models.Model):
    """
     班次列表详细时刻表
    """
    _name = 'bus_shift_line_detail'

    shift_line_id = fields.Many2one('bus_shift_line', ondelete='cascade')
    start_time = fields.Char(required=True)
    end_time = fields.Char(required=True)

