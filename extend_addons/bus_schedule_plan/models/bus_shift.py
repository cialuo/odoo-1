# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import re


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
    sequence = fields.Integer("Shift Line Sequence", default=0, required=True, readonly=True)
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
        reg = '^(0\d{1}|1\d{1}|2[0-3]):([0-5]\d{1})$'
        for i in self:
            for j in i.detail_ids:
                if j.start_time:
                    if not re.match(reg, j.start_time):
                        raise exceptions.ValidationError(_("Time format is not correct"))
                if j.end_time:
                    if not re.match(reg, j.end_time):
                        raise exceptions.ValidationError(_("Time format is not correct"))


class BusShiftLineDetail(models.Model):
    """
     班次列表详细时刻表
    """
    _name = 'bus_shift_line_detail'

    shift_line_id = fields.Many2one('bus_shift_line', ondelete='cascade')
    start_time = fields.Char(required=True)
    end_time = fields.Char(required=True)





