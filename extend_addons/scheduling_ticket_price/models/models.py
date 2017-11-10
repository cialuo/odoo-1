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
                                  ('down', 'down')], default='up', required=True)

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
        <?xml version="1.0" encoding="gbk"?> \r\n
        <TicketPrice> \r\n
            <Tickets Dir="1"> \r\n
                %s
            <Tickets> \r\n
            <Tickets Dir="0"> \r\n
                %s
            <Tickets> \r\n
        </TicketPrice> \r\n
        """
        up_str = ''
        down_str = ''
        for i in res:
            tmp_str = """
                <Item StartSt="%s" StartStID="%s" EndSt="%s" EndStID="%s" Price="%s" /> \r\n
            """ % (i.start_station_id.station_id.name,
                                i.start_station_id.station_id.code,
                                i.end_station_id.station_id.name,
                                i.end_station_id.station_id.code,
                                str(i.price))
            if i.direction == 'up':
                up_str += tmp_str
            else:
                down_str += tmp_str
        xml_str = xml_str % (up_str, down_str)
        self.write({'ticket_price_xml':xml_str})
        return self


