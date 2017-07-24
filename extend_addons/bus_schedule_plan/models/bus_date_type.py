# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BusDateType(models.Model):
    """
     日期类型管理
    """
    _name = 'bus_date_type'

    name = fields.Char('Date Name', required=True)
    type = fields.Selection([('Monday', "Monday"),
                            ('Tuesday', "Tuesday"),
                            ('Wednesday', "Wednesday"),
                            ('Thursday', "Thursday"),
                            ('Friday', "Friday"),
                            ('Saturday', "Saturday"),
                            ('Sunday', "Sunday"),
                            ('Minor Vacation', 'Minor Vacation'),
                            ('Long Vacation', 'Long Vacation'),
                             ], default='Monday',
                            )

    priority = fields.Selection([('one level','one level'),
                                 ('two level', 'two level'),
                                 ], default='two level')

    start_date = fields.Date()
    end_date = fields.Date()