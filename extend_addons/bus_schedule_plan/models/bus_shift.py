# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BusShift(models.Model):
    """
     班制管理
    """
    _name = 'bus_shift'

    name = fields.Char('Shift Name', required=True)
    shift_ct = fields.Integer(compute='_get_shift_ct')
    shift_line_ids = fields.One2many('bus_shift_choose_line', 'shift_id')

    @api.depends('shift_line_ids')
    def _get_shift_ct(self):
        for i in self:
            i.shift_ct = len(i.shift_line_ids)


class BusShiftChooseLine(models.Model):
    """
     班制 班次详情
    """
    _name = 'bus_shift_choose_line'
    _rec_name = 'shift_line_id'

    shift_id = fields.Many2one('bus_shift', ondelete='cascade')
    sequence = fields.Integer("Shift Line Sequence", default=1)
    shift_line_id = fields.Many2one('bus_shift_line')


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


class BusShiftLineDetail(models.Model):
    """
     班次列表详细时刻表
    """
    _name = 'bus_shift_line_detail'

    shift_line_id = fields.Many2one('bus_shift_line', ondelete='cascade')
    start_time = fields.Char()
    end_time = fields.Char()





