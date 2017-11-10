# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TicketPrice(models.Model):
    _name = 'opertation_resources_ticket_price'

    start_station_id = fields.Many2one('opertation_resources_station_platform', ondelete='cascade',
                                       string="Start Station", required=True) #起点站台
    end_station_id = fields.Many2one('opertation_resources_station_platform', ondelete='cascade',
                                       string="End Station", required=True) #终点站台
    route_id = fields.Many2one('route_manage.route_manage', ondelete='cascade', string='Route Choose',
                               required=True) #线路id
    price = fields.Float(string='Ticket Price') #票价
    direction = fields.Selection([('up', 'up'),
                                  ('down', 'down')], default='up')

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class route_manage(models.Model):
    _inherit = 'route_manage.route_manage'

    ticket_price_xml = fields.Text(string='ticket price xml', default='')
    ticket_price_relation = fields.One2many('opertation_resources_ticket_price', 'route_id', string='ticket price relation')

    def generate_xml(self):
        res = self.ticket_price_relation
        xml_str = """
        <?xml version="1.0" encoding="gbk"?>
            <TicketPrice>
                <Tickets Dir="1">
                    <Item StartSt="" StartStID="" EndSt="" EndStID="" Price="" />
                <Tickets>"""

        for i in res:
            dir = '1' if i.direction == 'up' else '0'
            xml_str += """
            <Tickets Dir="%s">
                <Item StartSt="%s" StartStID="%s" EndSt="%s" EndStID="%s" Price="%s" />
            <Tickets>""" % (dir, i.start_station_id.station_id.name,
                                i.start_station_id.station_id.code,
                                i.end_station_id.station_id.name,
                                i.end_station_id.station_id.code,
                                str(i.price))
        xml_str += "</TicketPrice>"
        self.write({'ticket_price_xml':xml_str})
        return self


