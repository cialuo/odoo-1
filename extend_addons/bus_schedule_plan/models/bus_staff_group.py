# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusStaffGroup(models.Model):
    """
    人车配班
    """
    _name = 'bus_staff_group'
    name = fields.Char()


class BusStaffGroupLine(models.Model):
    """
    人车配班详情
    """
    _name = 'bus_staff_group_line'
    name = fields.Char()

