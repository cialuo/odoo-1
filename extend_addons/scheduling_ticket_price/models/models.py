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

    ticket_price_relation = fields.One2many('opertation_resources_ticket_price', 'route_id', string='ticket price relation')

    def generate_xml(self, vals):
        res = self.env['opertation_resources_ticket_price'].search([('route_id', '=', vals['route_id'])])
        res2 = self.ticket_price_relation
        xml_str = """
        <?xml version="1.0" encoding="gbk"?>
            <TicketPrice>
                <Tickets Dir="1">
                    <Item StartSt="" StartStID="" EndSt="" EndStID="" Price="" />
                <Tickets>"""
        for i in res:
            dir = 1 if i.direction == 'up' else 'down'
            xml_str += """
            <Tickets Dir="{Dir}">
                <Item StartSt="{StartSt}" StartStID="{StartStID}" EndSt="{EndSt}" EndStID="{EndStID}" Price="{Price}" />
            <Tickets>""".format(Dir=str(dir), StartSt=i.start_station_id.station_id.name,
                                StartStID=i.start_station_id.station_id.code,
                                EndSt=i.end_station_id.station_id.name,
                                EndStID=i.end_station_id.station_id.code,
                                Price=i.price)
        xml_str += "</TicketPrice>"
        res_route = self.env['route_manage.route_manage'].search([('route_id', '=', vals['route_id'])])
        res_route.write({'ticket_price_xml':xml_str})
        return xml_str


