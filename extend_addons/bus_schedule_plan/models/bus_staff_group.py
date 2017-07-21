# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusStaffGroup(models.Model):
    _name = 'bus_staff_group'
    name = fields.Char()


class BusStaffGroupLine(models.Model):
    _name = 'bus_staff_group_line'
    name = fields.Char()

