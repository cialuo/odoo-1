# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusDateType(models.Model):
    """
     日期类型管理
    """
    _name = 'bus_date_type'

    name = fields.Char('Date Name', required=True)
    type = fields.Selection([('monday', "Monday"),
                            ('tuesday', "Tuesday"),
                            ('wednesday', "Wednesday"),
                            ('thursday', "Thursday"),
                            ('friday', "Friday"),
                            ('saturday', "Saturday"),
                            ('sunday', "Sunday"),
                            ('minor vacation', 'Minor Vacation'),
                            ('big vacation', 'Long Vacation'),
                             ], default='Monday',
                            )

    priority = fields.Selection([('one level','one level'),
                                 ('two level', 'two level'),
                                 ], default='two level')

    start_date = fields.Date()
    end_date = fields.Date()