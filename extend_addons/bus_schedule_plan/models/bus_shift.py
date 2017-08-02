# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BusShift(models.Model):
    """
     班制管理
    """
    _name = 'bus_shift'

    name = fields.Char('Shift Name', required=True)
    shift_ct = fields.Integer(compute='_get_shift_ct')
    shift_line_ids = fields.One2many('bus_shift_line', 'shift_id', "ShiftLines")

    @api.depends('shift_line_ids')
    def _get_shift_ct(self):
        for i in self:
            i.shift_ct = len(i.shift_line_ids)


class BusShiftLine(models.Model):
    """
     班次列表
    """
    _name = 'bus_shift_line'

    _sql_constraints = [
        ('sequence_unique', 'unique(sequence, shift_id)', _('The sequence must be unique!')),
        ('name_unique', 'unique(name, shift_id)', _('The name must be unique!'))
    ]

    shift_id = fields.Many2one('bus_shift')
    sequence = fields.Integer("Shift Line Sequence", default=1)
    name = fields.Char('Shift Line Name', required=True)
    start_time = fields.Char()
    end_time = fields.Char()






