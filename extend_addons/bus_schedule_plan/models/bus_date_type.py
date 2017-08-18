# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class BusDateType(models.Model):
    """
     日期类型管理
    """
    _name = 'bus_date_type'

    name = fields.Char(string='Date Type Name', required=True)
    type = fields.Selection([('Monday', "Monday"),
                            ('Tuesday', "Tuesday"),
                            ('Wednesday', "Wednesday"),
                            ('Thursday', "Thursday"),
                            ('Friday', "Friday"),
                            ('Saturday', "Saturday"),
                            ('Sunday', "Sunday"),
                            ('Vacation', 'Vacation'),
                            ], default='Monday', string='Date Type', required=True)

    priority = fields.Selection([('one level', 'one level'),
                                 ('two level', 'two level'),
                                 ], default='two level', readonly=True)

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    @api.onchange('type')
    def onchange_priority(self):
        for i in self:
            if i.type == 'Vacation':
                i.priority = 'one level'
            else:
                i.priority = 'two level'

    @api.constrains('start_date', 'end_date')
    def _check_change_count(self):
        for r in self:
            if r.start_date > r.end_date:
                raise exceptions.ValidationError(_("end_date must be greater than start_date"))

    def check_type_date(self, date_type, start_date, end_date, id=False):
        if id:
            res = self.search([('type', '=', date_type),('id', '!=', id)])
        else:
            res = self.search([('type', '=', date_type)])
        for i in res:
            if start_date >= i.start_date and start_date <= i.end_date:
                raise exceptions.ValidationError(_("date type have repeat of time"))
            elif start_date >= i.start_date and end_date <= i.end_date:
                raise exceptions.ValidationError(_("date type have repeat of time"))
            elif end_date >= i.start_date and end_date < i.end_date:
                raise exceptions.ValidationError(_("date type have repeat of time"))
            elif start_date <= i.start_date and end_date >= i.end_date:
                raise exceptions.ValidationError(_("date type have repeat of time"))

    @api.model
    def create(self, data):
        """
        报修单:
            功能：自动生成人车配班名称 线路名称/当前日期
        """
        date_type = data['type']
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise exceptions.ValidationError(_("end_date must be greater than start_date"))

        self.check_type_date(date_type, start_date, end_date)

        res = super(BusDateType, self).create(data)
        return res

    @api.multi
    def write(self, vals):
        if 'type' in vals or 'start_date' in vals or 'end_date' in vals:
            if 'type' in vals:
                date_type = vals.get('type', '')
            else:
                date_type = self.type
            if 'start_date' in vals:
                start_date = vals.get('start_date', '')
            else:
                start_date = self.start_date
            if 'end_date' in vals:
                end_date = vals.get('end_date', '')
            else:
                end_date = self.end_date
            if start_date > end_date:
                raise exceptions.ValidationError(_("end_date must be greater than start_date"))

            self.check_type_date(date_type, start_date, end_date, id=self.id)

        return super(BusDateType, self).write(vals)